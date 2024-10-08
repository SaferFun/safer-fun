use anchor_lang::prelude::*;

#[error_code]
pub enum SaferFunError {
    #[msg("Pool lifetime is too short")]
    PoolLifetimeTooShort,


    #[msg("Pool has already been initialized")]
    PoolAlreadyInitialized,
    #[msg("Pre buyer has already been initialized")]
    PreBuyerAlreadyInitialized,

    #[msg("Pool is not open")]
    PoolNotOpen,

    #[msg("Pool is not in a valid state to enter")]
    CannotEnterThePool,

    #[msg("Pool is not in a valid state to withdraw")]
    CannotWithdrawFromThePool,
    
    #[msg("Selected platfrom is invalid")]
    InvalidPlatfrom,

    #[msg("Invalid pool owner")]
    InvalidPoolOwner,

    #[msg("Invalid order lifetime")]
    InvalidOrderLifetime,

    #[msg("Invalid buy size")]
    InvalidBuySize,

    #[msg("Invalid withdraw size")]
    InvalidWithdrawSize,

    #[msg("Buyer not found")]
    BuyerNotFound,

    #[msg("Unmatched token size")]
    UnmatchedTokenSize,

   
}