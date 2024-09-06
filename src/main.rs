use clap::{Arg, Command};
use serde::Deserialize;
use serde_json;
use serde_yaml;
use std::process::Output;
use std::{fs, process::Command as ProcessCommand};

#[derive(Debug, Deserialize)]
struct Config {
    #[serde(rename = "application")]
    application_name: String,
    alias: std::collections::HashMap<String, String>,
}

fn read_config(file_path: &str) -> Result<Config, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(file_path)?;

    if file_path.ends_with(".json") {
        let config: Config = serde_json::from_str(&content)?;
        Ok(config)
    } else if file_path.ends_with(".yaml") {
        let config: Config = serde_yaml::from_str(&content)?;
        Ok(config)
    } else {
        Err("Unsupported file format".into())
    }
}

fn execute_command(app: &str, args: &[&str]) -> Result<Output, std::io::Error> {
    ProcessCommand::new(app).args(args).output()
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("AliasMate")
        .version("1.0")
        .author("Your Name")
        .about("Executes commands based on a config file and alias")
        .arg(
            Arg::new("config")
                .short('c')
                .long("config")
                .value_name("FILE")
                .help("Sets the configuration file (JSON or YAML)")
                .required(true),
        )
        .arg(
            Arg::new("args")
                .num_args(1..) // Accept one or more arguments
                .help("Arguments after --"),
        )
        .get_matches();

    // Get the config file path
    let config_file = matches
        .get_one::<String>("config")
        .expect("Config file is required");

    // Collect all arguments
    let args: Vec<&str> = matches
        .get_many::<String>("args")
        .unwrap_or_default()
        .map(String::as_str)
        .collect();

    // Read and parse the config file
    let config = read_config(config_file)?;

    println!("Parsed configuration: {:?}", config);

    // Split config.application_name into app_name and additional arguments
    let mut app_args: Vec<String> = config
        .application_name
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();
    let app_name = app_args.remove(0); // The first element is the app name

    // Translate arguments by replacing aliases from config and push them directly to app_args
    for arg in args {
        if let Some(alias_value) = config.alias.get(arg) {
            app_args.push(alias_value.clone());
        } else {
            app_args.push(arg.to_string());
        }
    }

    // Join all arguments into a single string with spaces
    let command_args_str = app_args.join(" ");

    // Execute the command
    println!("Executing command: {} {}", app_name, &command_args_str,);

    let output = execute_command(
        app_name.as_str(),
        &command_args_str.split_whitespace().collect::<Vec<&str>>(),
    )?;

    // Display the output
    println!(
        "Command stdout: {}",
        String::from_utf8_lossy(&output.stdout)
    );
    println!(
        "Command stderr: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    println!("Command exit status: {}", output.status);

    // Exit with the appropriate status code
    if output.status.success() {
        std::process::exit(0); // Exit with code 0 if successful
    } else {
        // Exit with the command's exit code, or 1 if none is available
        std::process::exit(output.status.code().unwrap_or(1));
    }
}
