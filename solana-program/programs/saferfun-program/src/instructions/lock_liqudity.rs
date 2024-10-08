use std::str::FromStr;

use anchor_lang::prelude::*;
use anchor_lang::solana_program::instruction::Instruction;
use anchor_lang::solana_program::program::invoke;
use anchor_spl::token::{Mint, TokenAccount,Token};
use crate::buyer::PreBuyer;
use crate::constants::{JITO_RESERVE_STAKE_ACCOUNT, JITO_STAKE_POOL_FEE_ACCOUNT, JITO_STAKING_POOL, JITO_STAKING_POOL_WITHDRAW_AUTHORITY, JITO_TOKEN_MINT, STAKING_POOL_PROGRAM};
use crate::pool::Pool;
use crate::seeds::{ POOL_ACCOUNT, POOL_PRE_BUYER, STAKE_MANAGER_ACCOUNT };
use crate::stake_manager::StakeManager;
use crate::traits::StakeJito;
use crate::SaferFunError;


#[derive(Accounts)]
#[instruction(data: LockLiqudityData)]
pub struct LockLiqudity<'info> {
    #[account(
        seeds = [POOL_ACCOUNT, &pool_owner.key.to_bytes()],
        bump = pool.bump,
        constraint = pool.pool_owner == *pool_owner.key,
        mut,
    )]
    pub pool: Account<'info, Pool>,
    #[account(
        init_if_needed,
        payer = pre_buyer,
        seeds = [POOL_PRE_BUYER, pool.key().as_ref(), pre_buyer.key().as_ref()],
        bump,
        space = 8 + PreBuyer::INIT_SPACE
    )]
    pub pre_buyer_escrow: Account<'info, PreBuyer>,
    #[account(
        seeds = [STAKE_MANAGER_ACCOUNT],
        bump = stake_manager.bump,
    )]
    pub stake_manager: Account<'info,StakeManager>,


    #[account(mut)]
    pub pre_buyer: Signer<'info>,
    /// CHECK: This is just for the seed, we don't need to use it
    pub pool_owner: AccountInfo<'info>, // just for the seed



    // ---- Accounts for jito stake ----
    #[account(address = Pubkey::from_str(STAKING_POOL_PROGRAM).unwrap())]
    pub staking_program: AccountInfo<'info>,

    #[account(address = Pubkey::from_str(JITO_STAKING_POOL).unwrap())]
    pub jito_staking_pool: AccountInfo<'info>,

    #[account(address = Pubkey::from_str(JITO_STAKING_POOL_WITHDRAW_AUTHORITY).unwrap())]
    pub jito_withdraw_authority: AccountInfo<'info>,

    #[account(address = Pubkey::from_str(JITO_RESERVE_STAKE_ACCOUNT).unwrap())]
    pub jito_reserve_authority: AccountInfo<'info>,

    #[account(address = Pubkey::from_str(JITO_STAKE_POOL_FEE_ACCOUNT).unwrap())]
    pub jito_fee_account: AccountInfo<'info>,

    #[account(mut)]
    pub stake_manager_ata: Account<'info,TokenAccount>,

    #[account(
        constraint = jito_token_mint.key() == Pubkey::from_str(JITO_TOKEN_MINT).unwrap()
    )]
    pub jito_token_mint: Account<'info,Mint>,


    //----------------------

    pub token_program: Program<'info,Token>,
    pub system_program: Program<'info, System>,
}
// depositor is not pool owner in this case therefore different implementation
impl StakeJito for LockLiqudity<'_> {
    fn stake_jito(&self, deposit_amount: u64) {
        let ix_data = {
            let mut buf = vec![];
            buf.push(14); // The discriminator for `DepositSol`
            buf.extend_from_slice(&deposit_amount.to_le_bytes());
            buf
        };

        let ix = Instruction {
            program_id: self.staking_program.key(),
            accounts: vec![
                AccountMeta::new(self.jito_staking_pool.key(), false),
                AccountMeta::new_readonly(self.jito_withdraw_authority.key(), false),
                AccountMeta::new(self.jito_reserve_authority.key(), false),
                AccountMeta::new(self.pre_buyer.key(), true),
                AccountMeta::new(self.stake_manager_ata.key(), false), //TODO: check if this possible a token account other than the depositor
                AccountMeta::new(self.jito_fee_account.key(), false),
                AccountMeta::new(self.stake_manager_ata.key(), false),
                AccountMeta::new(self.jito_token_mint.key(), false),
                AccountMeta::new_readonly(self.system_program.key(), false),
                AccountMeta::new_readonly(self.token_program.key(), false)
            ],
            data: ix_data,
        };

        invoke(&ix, &[
            self.staking_program.clone(),
            self.jito_staking_pool.clone(),
            self.jito_withdraw_authority.clone(),
            self.jito_reserve_authority.clone(),
            self.pre_buyer.to_account_info(),
            self.stake_manager_ata.to_account_info(),
            self.jito_fee_account.clone(),
            self.jito_token_mint.to_account_info().clone(),
            self.token_program.to_account_info(),
            self.system_program.to_account_info(),
        ]).unwrap();
    }
}

#[derive(AnchorDeserialize, AnchorSerialize)]
pub struct LockLiqudityData {
    pub token_amount: u64,
    pub bid_amount: u64,
    
}

pub fn handler(
    ctx: Context<LockLiqudity>,
    data:LockLiqudityData
) -> Result<()> {
    let LockLiqudityData {
        token_amount,
        bid_amount
    } = data;

    require_gt!(token_amount, 0, SaferFunError::InvalidBuySize);
    
    //jito stake to stake manager

    //TODO:maybe modularize this
    let deposit_amount = token_amount + bid_amount;
    ctx.accounts.stake_jito(deposit_amount);

    //-------------------

    // necessary data registrations for buyer
    let pre_buyer_escrow = &mut ctx.accounts.pre_buyer_escrow;
    let pre_buyer = &mut ctx.accounts.pre_buyer;
    let pool = &mut ctx.accounts.pool;
    pre_buyer_escrow.init(pre_buyer.key, pool)?;

    pool.add_buyer(
        pre_buyer_escrow,
        token_amount,
        bid_amount,
    )?;
    //------------------------
    msg!("new buyer added successfully");
    Ok(())
}

