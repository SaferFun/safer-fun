use anchor_lang::prelude::*;

pub mod constants;
pub mod instructions;
pub mod errors;
pub mod events;
pub mod state;
pub mod utils;
pub mod traits;
pub mod seeds;


use instructions::*;
use errors::*;
use events::*;
use state::*;

declare_id!("9BynGY4JA6k8wJaPjg7JH6YQ4aEHbWqvx62zZT3x6ugc");

#[program]
pub mod saferfun_program {

    use super::*;

   pub fn create_pool(ctx:Context<CreatePool>, data:CreatePoolData) -> Result<()> {
        msg!("Create Pool");
        create_pool::handler(ctx, data)
   }

   pub fn lock_liqudity(ctx:Context<LockLiqudity>, data:LockLiqudityData) -> Result<()> {
        msg!("Lock Liqudity");
        lock_liqudity::handler(ctx, data)
   }
   pub fn withdraw_liqudity(ctx:Context<WithdrawLiqudity>) -> Result<()> {
        msg!("Withdraw Liqudity");
        withdraw_liqudity::handler(ctx)
   }
   
}