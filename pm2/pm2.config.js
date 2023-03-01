const path = require("path");

if (process.platform === "win32") {
    scrapy_script = path.join("..", "src", ".venv", "Scripts", "scrapy.exe");
    python_interpreter = path.join("..", "src", ".venv", "Scripts", "python.exe");
}
else {
    scrapy_script = path.join("..", "src", ".venv", "bin", "scrapy");
    python_interpreter = path.join("..", "src", ".venv", "bin", "python");
}

module.exports = {
    apps: [
        {
            name: "eab_session_runner",
            script: scrapy_script,
            interpreter: python_interpreter,
            args: "session_runner",
            cwd: path.join("..", "src"),
            log_file: path.join("..", "logs", "eab_session_runner.log"),
            cron_restart: "*/30 * * * *",
            autorestart: false
        }
    ]
}
