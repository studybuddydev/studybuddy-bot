import { Telegraf } from "telegraf";
import { message } from 'telegraf/filters';
import * as dotenv from 'dotenv';
import axios from 'axios';
import { parse } from 'node-html-parser';
import fs from 'fs';
import { Client } from '@notionhq/client'


dotenv.config();


const notion = new Client({ auth: process.env.NOTION_TOKEN });
const db_id = process.env.DB_ID ?? '';
const tododev_id = process.env.TODODEV_ID ?? '';


const bot = new Telegraf(process.env.BOT_TOKEN ?? '');

bot.start((ctx) => ctx.reply('ciao sono studybuddy'));


bot.command('ping', (ctx) => ctx.reply('pong'));

bot.command('todo', async (ctx) => {
    const todos = await getTodos()

    ctx.reply(todos.join('\n'))


});
async function check() {
    console.log('ciao')
}

//setInterval(() => check(), 1000 );



async function getTodos() {
    const response = await notion.databases.query({
        database_id: tododev_id,
    });

    let todos = []
    
    for (const page of response.results as any) {
        if (page['properties']['Status']['status']['name'] != 'Done'){
            if (page.properties.priority?.select?.name != 'low' && page.properties.priority?.select?.name){
                
                //console.log(page.properties.priority?.select?.name)
                //console.log(page['properties']['Name']['title'][0]['plain_text']);
                todos.push(page['properties']['Name']['title'][0]['plain_text'])
                //console.log(page['properties'])
            }
        }
    }
    return todos
}

process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
bot.launch();
console.log('Bot started');