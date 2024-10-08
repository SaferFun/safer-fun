use anchor_lang::prelude::*;
use crate::buyer::PreBuyer;
use crate::pool::Pool;
use crate::seeds::{ POOL_ACCOUNT, POOL_PRE_BUYER, STAKE_MANAGER_ACCOUNT };
use crate::stake_manager::StakeManager;


#[derive(Accounts)]
pub struct WithdrawLiqudity<'info> {
    #[account(
        seeds = [POOL_ACCOUNT, &pool_owner.key.to_bytes()],
        bump = pool.bump,
        constraint = pool.pool_owner == *pool_owner.key,
        mut,
    )]
    pub pool: Account<'info, Pool>,
    #[account(
        seeds = [POOL_PRE_BUYER, pool.key().as_ref(), pre_buyer.key().as_ref()],
        bump = pre_buyer_escrow.bump,
        mut,
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
    pub system_program: Program<'info, System>,
}

//Only allow full withdrawl
pub fn handler(
    ctx: Context<WithdrawLiqudity>,
) -> Result<()> {

    let pre_buyer_escrow = &mut ctx.accounts.pre_buyer_escrow;
    let pre_buyer = &mut ctx.accounts.pre_buyer;
    let pool = &mut ctx.accounts.pool;
    let stake_manager = &mut ctx.accounts.stake_manager;
   

   //On-chain transfer has been made from stake manager to user in remove_buyer
    pool.remove_buyer(
        pre_buyer_escrow,
        stake_manager,
        pre_buyer.to_account_info()
    )?;
    msg!("buyer removed successfully");
    Ok(())
}

