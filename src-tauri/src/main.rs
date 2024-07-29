// Prevents additional console window on Windows in release, DO NOT REMOVE!!
// #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager};
use std::process::Command;


fn main() {

  tauri::Builder::default()
    .setup(|app| {
        Ok(())
    })

    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
