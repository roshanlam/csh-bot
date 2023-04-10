// write a discord bot in typescript

import { Client } from "discord.js";
import { config } from "dotenv";
import mongoose from "mongoose";

const uri = "mongodb+srv://roshandiscordbot:<password>@cluster0.2bwyiqk.mongodb.net/?retryWrites=true&w=majority";

mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log("Connected to MongoDB"))
    .catch((err) => console.log(err));


const client =  new Client();

client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`);
    }
);

client.login(process.env.TOKEN);

