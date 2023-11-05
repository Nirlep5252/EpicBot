use dotenv::dotenv;
use poise::serenity_prelude as serenity;

struct Data {}
type Error = Box<dyn std::error::Error + Send + Sync>;
type Context<'a> = poise::Context<'a, Data, Error>;

#[poise::command(slash_command, prefix_command)]
async fn hello(ctx: Context<'_>) -> Result<(), Error> {
    ctx.say("world").await?;
    Ok(())
}

async fn on_error(error: poise::FrameworkError<'_, Data, Error>) {
    match error {
        poise::FrameworkError::UnknownCommand {
            ctx,
            msg,
            prefix,
            msg_content,
            invocation_data,
            trigger,
            ..
        } => {
            dbg!(&msg, &prefix, &msg_content, &invocation_data, &trigger);
            // TODO: use this to check whether this unknown cmd is a custom command or not
            println!("INFO: Unknown cmd");
        }
        error => {
            if let Err(err) = poise::builtins::on_error(error).await {
                println!("ERROR: {}", err);
            }
        }
    }
}

#[tokio::main]
async fn main() {
    dotenv().ok();

    println!("INFO: Starting bot");

    // TODO: add database
    poise::Framework::builder()
        .options(poise::FrameworkOptions {
            commands: vec![hello()],
            on_error: |error| Box::pin(on_error(error)),
            ..Default::default()
        })
        .token(std::env::var("TOKEN").expect("ERROR: Missing TOKEN env var"))
        .intents(
            serenity::GatewayIntents::non_privileged()
                | serenity::GatewayIntents::GUILD_MEMBERS
                | serenity::GatewayIntents::GUILD_MESSAGES,
        )
        .setup(|ctx, _ready, framework| {
            Box::pin(async move {
                poise::builtins::register_globally(ctx, &framework.options().commands).await?;
                Ok(Data {})
            })
        })
        .run()
        .await
        .unwrap();
}
