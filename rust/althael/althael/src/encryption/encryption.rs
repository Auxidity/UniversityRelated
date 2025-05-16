use aes::Aes128;
use block_modes::{BlockMode, Cbc};
use block_modes::block_padding::Pkcs7;
use hmac::{Hmac, Mac};
use rand::Rng;
use sha2::{Sha256, Digest};
use std::error::Error;
use serde_json::{Value, from_slice};

type Aes128Cbc = Cbc<Aes128, Pkcs7>;
type HmacSha256 = Hmac<Sha256>;

#[allow(dead_code)]
pub fn generate_salt(password: &str) -> String {
    format!("{:x}", Sha256::digest(password.as_bytes()))
}

#[allow(dead_code)]
pub fn encrypt(data: &str, password: &str) -> Result<Vec<u8>, Box<dyn Error>> {
    let salt = password;
    let key = &salt.as_bytes()[..16];
    let iv = rand::thread_rng().gen::<[u8; 16]>();

    let cipher = Aes128Cbc::new_from_slices(key, &iv)?;
    let encrypted_data = cipher.encrypt_vec(data.as_bytes());

    let mut hmac = HmacSha256::new_from_slice(key)?;
    hmac.update(&encrypted_data);
    let hmac_value = hmac.finalize().into_bytes();

    let mut result = Vec::new();
    result.extend_from_slice(&iv);
    result.extend_from_slice(&encrypted_data);
    result.extend_from_slice(&hmac_value);

    Ok(result)
}

#[allow(dead_code)]
pub fn decrypt(encrypted_data: &[u8], password: &str) -> Result<Value, Box<dyn Error>> {
    if encrypted_data.len() < 48 {
            return Err("Encrypted data is too short. Expected at least 48 bytes.".into());
        }   

    let salt = password;
    let key = &salt.as_bytes()[..16];

    // Extract the IV, encrypted data, and HMAC
    let iv = &encrypted_data[..16];
    let hmac_value = &encrypted_data[encrypted_data.len() - 32..];
    let cipher_data = &encrypted_data[16..encrypted_data.len() - 32];

    // Verify HMAC
    let mut hmac = HmacSha256::new_from_slice(key)?;
    hmac.update(cipher_data);
    hmac.verify(hmac_value.into())?;

    // Decrypt data
    let cipher = Aes128Cbc::new_from_slices(key, iv)?;
    let decrypted_data = cipher.decrypt_vec(cipher_data)?;

    // Attempt to parse decrypted data as JSON
    let json_data: Value = from_slice(&decrypted_data)?;

    Ok(json_data)
}

