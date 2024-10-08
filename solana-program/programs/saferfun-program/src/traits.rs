use std::str::FromStr;

use anchor_lang::{ prelude::{AccountInfo, AccountMeta, Pubkey}, solana_program::instruction::Instruction, Key };

use crate::{ constants::JITO_TOKEN_MINT, CreatePool, LockLiqudity };

pub trait StakeJito {
    fn stake_jito(&self, deposit_amount: u64); // Example of a common field or method
}
