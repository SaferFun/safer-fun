use anchor_lang::prelude::*;
use anchor_lang::solana_program::program::invoke;
use anchor_lang::solana_program::stake;

use crate::{ constants::MIN_POOL_LIFETIME, SaferFunError };

use crate::utils::calculate_auction_score;

use super::buyer::{self, PreBuyer};
use super::stake_manager::StakeManager;

#[account]
#[derive(Default, InitSpace)]
pub struct Pool {
    pub pool_owner: Pubkey,
    pub target_platform: Platform,
    #[max_len(30)] // max 30 pubkeys for now
    pub buyers: Vec<Pubkey>,
    pub metadata: Metadata,
    pub pool_release_date: i64,
    pub created_at: i64,
    pub pool_status: PoolStatus,
    pub bump: u8,
}

impl Pool {
    pub fn init(
        &mut self,
        pool_owner: &Pubkey,
        target_platfrom: Platform,
        metadata: Metadata,
        pool_release_date: i64
    ) -> Result<()> {
        msg!("{}",self.pool_status as u8);
        require_eq!(
            self.pool_status as u8,
            PoolStatus::Init as u8,
            SaferFunError::PoolAlreadyInitialized
        );
        let clock = Clock::get()?;
        require_gt!(
            pool_release_date,
            clock.unix_timestamp + MIN_POOL_LIFETIME,
            SaferFunError::PoolLifetimeTooShort
        );
        self.pool_owner = *pool_owner;
        self.target_platform = target_platfrom;
        self.metadata = metadata;
        self.pool_release_date = pool_release_date;
        self.buyers = vec![];
        self.pool_status = PoolStatus::Open;
        Ok(())
    }
    pub fn add_buyer<'a>(
        &mut self,
        pre_buyer: &mut Account<'a,PreBuyer>,
        locked_amount: u64,
        bid_amount: u64,
    ) -> Result<()> {
        require_eq!(self.pool_status as u8, PoolStatus::Open as u8, SaferFunError::PoolNotOpen);
        require!(self.can_enter(), SaferFunError::CannotEnterThePool);

        let curr_time = Clock::get()?.unix_timestamp;
        let auction_score = calculate_auction_score(bid_amount, locked_amount, self.pool_release_date,curr_time );

        pre_buyer.add_locked_size(locked_amount)?;
        pre_buyer.set_status(buyer::BuyerStatus::Locked)?;
        pre_buyer.auction_score = auction_score; //TODO: make sure to wheter use encapulation or not
        
        self.buyers.push(pre_buyer.key());
        Ok(())
    }
    pub fn remove_buyer<'a>(&mut self,pre_buyer: &mut Account<'a,PreBuyer>,stake_manager: &mut Account<'a,StakeManager>,buyer: AccountInfo<'a>) -> Result<()> {
        
        require!(self.can_withdraw(), SaferFunError::CannotWithdrawFromThePool);
        require_eq!(self.pool_status as u8, PoolStatus::Open as u8, SaferFunError::PoolNotOpen);
        require!(self.buyers.contains(buyer.key), SaferFunError::BuyerNotFound);


        
        let amount = pre_buyer.get_locked_size();

        /*TODO:
        check if stake_manager has enough lamports 
        else unstake from stake_manager and transfer to buyer
        */
        **stake_manager.to_account_info().try_borrow_mut_lamports()? -= amount;
        **buyer.try_borrow_mut_lamports()? += amount;

        pre_buyer.set_status(buyer::BuyerStatus::Withdrawn)?;
        self.buyers.retain(|x| x != buyer.key);        
        Ok(())
    }
    pub fn is_open(&self) -> bool {
        self.pool_status == PoolStatus::Open
    }
    pub fn can_enter(&self) -> bool {
        match self.pool_status {
            PoolStatus::Open => true,
            _ => false,
        }
    }
    pub fn can_withdraw(&self) -> bool {
        match self.pool_status {
            PoolStatus::Open | PoolStatus::OnlyWithdraw => true,
            _ => false,
        }
    }
    pub fn can_cancel(&self) -> bool {
        match self.pool_status {
            PoolStatus::Open => true,
            _ => false,
        }
    }
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone, PartialEq, Eq, Default, InitSpace)]
pub enum Platform {
    #[default]
    Pumpfun,
    Raydium,
    Meteora,
    Moonshot,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq, Eq, Default, InitSpace)]
pub struct Metadata {
    #[max_len(20)]
    pub name: String,
    #[max_len(50)]
    pub description: String,
    #[max_len(80)]
    pub image_url: String,
    #[max_len(80)]
    pub social_urls: [String;4],
}

#[derive(AnchorSerialize, AnchorDeserialize, Copy, Clone, PartialEq, Eq, Default, InitSpace)]
pub enum PoolStatus {
    #[default]
    Init,
    Open,
    OnDistribution,
    OnlyWithdraw,
    Cancelled,
    Finished,
}
