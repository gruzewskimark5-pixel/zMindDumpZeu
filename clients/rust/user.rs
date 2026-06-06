// Example code that deserializes and serializes the model.
// extern crate serde;
// #[macro_use]
// extern crate serde_derive;
// extern crate serde_json;
//
// use generated_module::user;
//
// fn main() {
//     let json = r#"{"answer": 42}"#;
//     let model: user = serde_json::from_str(&json).unwrap();
// }

use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct User {
    title: String,

    description: String,

    #[serde(rename = "type")]
    user_type: String,

    properties: Properties,

    required: Vec<String>,
}

#[derive(Serialize, Deserialize)]
pub struct Properties {
    id: Email,

    username: Username,

    email: Email,
}

#[derive(Serialize, Deserialize)]
pub struct Email {
    #[serde(rename = "type")]
    email_type: String,

    format: String,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Username {
    #[serde(rename = "type")]
    username_type: String,

    min_length: i64,
}
