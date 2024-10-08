use std::str::FromStr;

use anchor_lang::prelude::*;

#[constant]
pub const MIN_POOL_LIFETIME: i64 = 1800;
#[constant]
pub const ONLY_WITHDRAW_STATE_DURATION: i64 = 300;

pub const STAKING_POOL_PROGRAM: &str = "SPoo1Ku8WFXoNDMHPsrGSTSG1Y47rzgn41SLUNakuHy";
pub const JITO_STAKING_POOL: &str = "Jito4APyf642JPZPx3hGc6WWJ8zPKtRbRs4P815Awbb";
pub const JITO_STAKING_POOL_WITHDRAW_AUTHORITY: &str = "6iQKfEyhr3bZMotVkW6beNZz5CPAkiwvgV2CTje9pVSS";
pub const JITO_RESERVE_STAKE_ACCOUNT: &str = "BgKUXdS29YcHCFrPm5M8oLHiTzZaMDjsebggjoaQ6KFL";
pub const JITO_STAKE_POOL_FEE_ACCOUNT: &str = "feeeFLLsam6xZJFc6UQFrHqkvVt4jfmVvi2BRLkUZ4i";
pub const JITO_TOKEN_MINT: &str = "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn";