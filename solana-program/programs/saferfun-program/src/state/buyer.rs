

use anchor_lang::prelude::*;

use crate::{pool::PoolStatus, SaferFunError};
use super::pool::Pool;

#[account]
#[derive(Default, InitSpace)]
pub struct PreBuyer {
    pub buyer: Pubkey, 
    pub bump: u8,
    pub locked_amount: u64, 
    pub locked_bid: u64,
    pub target_pool: Pubkey,
    pub status: BuyerStatus,
    pub auction_score: u64,
    pub is_dev: bool,
}

impl PreBuyer {

    pub fn init(&mut self,buyer:&Pubkey,target_pool: &Account<Pool>) -> Result<()> {
        if self.status == BuyerStatus::Init {   
            // Add pool based checks
            require_eq!(target_pool.pool_status as u8, PoolStatus::Open as u8);
            self.status = BuyerStatus::Locked;
            self.is_dev = target_pool.pool_owner == *buyer;
            self.buyer = *buyer;
            self.target_pool = *target_pool.to_account_info().key;
            self.locked_amount = 0;
            self.locked_bid = 0;
            self.auction_score = 0;
        }
            
        Ok(())
    }

    //TODO: check for overflow and underflow errors
    pub fn add_locked_size(&mut self, amount: u64) -> Result<()> {
        require_eq!(self.status as u8, BuyerStatus::Locked as u8);
        self.locked_amount += amount;
        Ok(())
    }
    pub fn remove_all_locked_size(&mut self) -> Result<()> {
        require_eq!(self.status as u8, BuyerStatus::Locked as u8);
        self.locked_amount =0;
        Ok(())
    }

    pub fn get_locked_size(&self) -> &u64 {
        &self.locked_amount
    }

    pub fn set_status(&mut self, status: BuyerStatus) -> Result<()> {
        self.status = status;
        Ok(())
    }
    pub fn get_status(&self) -> &BuyerStatus {
        &self.status
    }

    
}

#[derive(
    AnchorSerialize, AnchorDeserialize, Copy, Clone, PartialEq, Eq, Default, InitSpace
)]
pub enum BuyerStatus {
    #[default]
    Init,
    Locked,
    Withdrawn,
    OnDistribution,
    Completed,
}