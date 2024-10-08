use anchor_lang::prelude::*;

use crate::{ constants::MIN_POOL_LIFETIME, SaferFunError };

use crate::utils::{calculate_auction_score, get_plafrom_fee};
use anchor_lang::system_program;

use super::buyer::{self, PreBuyer};

#[account]
#[derive(Default, InitSpace)]
pub struct StakeManager {
    pub seed: u64,
    pub bump: u8,
}
