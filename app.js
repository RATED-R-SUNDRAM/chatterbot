process.env["NTBA_FIX_319"] = 1;
var port = process.env.PORT || 3000;
const telegrambot = require('node-telegram-bot-api');
const Promise = require('bluebird');
Promise.config({
    cancellation: true
});

var token = "1415465961:AAHbf0zop4xQVTUf4Cg5Qc5_RqCTXtz6zwg"
const bot = new telegrambot(token, { polling: true });




bot.on('message', (msg) => {
    data = [msg.chat.first_name, msg.text];
    ms_g = data[1]
    console.log(data);
    var spawn = require('child_process').spawn;
    py = spawn('python', ['chat.py'])
    py.stdout.on('data', (data) => {
        names = data.toString();
        console.log(names);
        bot.sendMessage(msg.chat.id, names)
    });
    py.stdin.write(JSON.stringify(ms_g));
    py.stdin.end();

});
app.listen(port, () => { console.log("sexy") })