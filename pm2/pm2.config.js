const path = require("path");

if (process.platform === "win32") scrapy_script = path.join("..", "src", ".venv", "Scripts", "scrapy.exe");
else scrapy_script = path.join("..", "src", ".venv", "bin", "scrapy");

module.exports = {
    apps: [
        {
            name: "eab_session_runner",
            script: scrapy_script,
            args: "session_runner",
            cwd: path.join("..", "src"),
            log_file: path.join("..", "logs", "eab_session_runner.log"),
            cron_restart: "*/30 * * * *",
            autorestart: false
        }
    ]
}
