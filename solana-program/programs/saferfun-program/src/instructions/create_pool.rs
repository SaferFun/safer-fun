use std::str::FromStr;

use anchor_lang::prelude::*;
use anchor_lang::solana_program::instruction::Instruction;
use anchor_lang::solana_program::program::invoke;
use anchor_spl::token::{Mint, Token, TokenAccount};
use crate::buyer::PreBuyer;
use crate::constants::{JITO_RESERVE_STAKE_ACCOUNT, JITO_STAKE_POOL_FEE_ACCOUNT, JITO_STAKING_POOL, JITO_STAKING_POOL_WITHDRAW_AUTHORITY, JITO_TOKEN_MINT, STAKING_POOL_PROGRAM};
use crate::pool::{ Metadata, Platform, Pool };
use crate::seeds::{ POOL_ACCOUNT, POOL_PRE_BUYER, STAKE_MANAGER_ACCOUNT };
use crate::stake_manager::StakeManager;
use crate::traits::StakeJito;
use crate::utils::{ is_platfrom_allowed};
use crate::SaferFunError;


//TODO: check if there is a way to modularize the necesary accounts for staking
#[derive(Accounts)]
#[instruction(data: CreatePoolData)]
pub struct CreatePool<'info> {
    #[account(
        init_if_needed,
        payer = pool_owner,
        space = 8 + Pool::INIT_SPACE,
        seeds = [POOL_ACCOUNT, &pool_owner.key.to_bytes()],
        bump
    )]
    pub pool: Account<'info, Pool>,
    #[account(
        init_if_needed,
        payer = pool_owner,
        seeds = [POOL_PRE_BUYER, pool.key().as_ref(), pool_owner.key().as_ref()],
        bump,
        space = 8 + PreBuyer::INIT_SPACE
    )]
    pub dev_escrow: Account<'info, PreBuyer>,
    #[account(mut)]
    pub pool_owner: Signer<'info>,
    
    #[account(
        seeds = [STAKE_MANAGER_ACCOUNT],
        bump = stake_manager.bump,
    )]
    pub stake_manager: Account<'info,StakeManager>,

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

    #[account(
        mut,
        associated_token::mint = jito_token_mint,
        associated_token::authority = stake_manager
    )]   
    pub stake_manager_ata: Account<'info,TokenAccount>,

    #[account(
        constraint = jito_token_mint.key() == Pubkey::from_str(JITO_TOKEN_MINT).unwrap()
    )]
    pub jito_token_mint: Account<'info,Mint>,


    //----------------------

    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

impl StakeJito for CreatePool<'_> {
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
                AccountMeta::new(self.pool_owner.key(), true),
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
            self.pool_owner.to_account_info(),
            self.stake_manager_ata.to_account_info(),
            self.jito_fee_account.clone(),
            self.jito_token_mint.to_account_info().clone(),
            self.token_program.to_account_info(),
            self.system_program.to_account_info(),
        ]).unwrap();
    }
}
#[derive(AnchorDeserialize, AnchorSerialize)]
pub struct CreatePoolData {
    pub target_platform: Platform,
    pub token_amount: u64,
    pub pool_release_date: i64,
    pub metadata: Metadata,
    
}


pub fn handler(
    ctx: Context<CreatePool>,
    data:CreatePoolData
) -> Result<()> {
    let CreatePoolData {
        target_platform,
        token_amount:initial_buy_size,
        pool_release_date,
        metadata,
    } = data;

   
    require!(is_platfrom_allowed(target_platform), SaferFunError::InvalidPlatfrom);
    require_gt!(initial_buy_size, 0, SaferFunError::InvalidBuySize);

    let deposit_amount = initial_buy_size;
    ctx.accounts.stake_jito(deposit_amount);
    

 

    let pool_owner = &ctx.accounts.pool_owner; // Immutable reference
    let pool = &mut ctx.accounts.pool; // Mutable reference
    let dev_escrow = &mut ctx.accounts.dev_escrow; // Mutable reference
    pool.init(&pool_owner.key(), target_platform, metadata, pool_release_date)?;
    dev_escrow.init(&pool_owner.key(), pool)?;

    pool.add_buyer(
        dev_escrow,
        initial_buy_size,
        0,
    )?;
    msg!("Pool created successfully");
    Ok(())
}

