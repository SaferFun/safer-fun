use std::{fmt::Error, str::FromStr};

use anchor_lang::{prelude::{AccountMeta, Context, Program, Pubkey}, solana_program::instruction::Instruction, Bump, Bumps};

use crate::{constants::{JITO_RESERVE_STAKE_ACCOUNT, JITO_STAKE_POOL_FEE_ACCOUNT, JITO_STAKING_POOL, JITO_STAKING_POOL_WITHDRAW_AUTHORITY, JITO_TOKEN_MINT, STAKING_POOL_PROGRAM}, pool::Platform, traits::StakeJito};

pub fn is_platfrom_allowed(platfrom:Platform) -> bool  {

    match platfrom {
        Platform::Pumpfun => true,
        _ => false
    }   
}

pub fn get_plafrom_fee(platfrom:Platform,amount:u64) -> u64 {
    match platfrom {
        Platform::Pumpfun => (amount/100 * 1) as u64, // 1% fee
        _ => 0
    }
}
pub fn safer_fee(platfrom:Platform,amount:u64) -> u64 {
    match platfrom {
        Platform::Pumpfun => (amount/100 * 1) as u64, // 1% fee
        _ => 0
    }
}

pub fn get_constant_withdraw_fee() -> u64 {
    0
}

pub fn calculate_auction_score(bid_amount: u64, sol_amount: u64, pool_release_timestamp: i64, bid_timestamp: i64) -> u64 {
    const BETA: f64 = 0.5;
    let bid_amount_f64 = bid_amount as f64;
    let sol_amount_f64 = sol_amount as f64;
    let time_ratio = (pool_release_timestamp - bid_timestamp) as f64 / pool_release_timestamp as f64;

    let auction_score = (bid_amount_f64 / sol_amount_f64) * (1.0 + BETA * time_ratio);
    auction_score as u64
}