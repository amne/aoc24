local dap = require("dap")

dap.adapters.lldb = {
    type = "executable",
    command = "/usr/bin/lldb-vscode-14", -- adjust as needed
    name = "lldb",
}

dap.adapters.python = {
    type = 'executable',
    command = 'python',
    args = { '-m', 'debugpy.adapter' }
}

dap.configurations.rust = {
   {
      name = "wait to attach",
      type = "lldb",
      request = "attach",
      program =  function()
            -- current buffer name
            return vim.fn.expand("%"):gsub("%.rs","")
        end,
      waitFor = true
    }
}

dap.configurations.python = {
    {
        type = 'python',
        request = 'launch',
        name = "Launch file",
        program = "${file}",
        pythonPath = function()
            return '/usr/bin/python3'
        end,
    },
    {
        type = 'python',
        request = 'attach',
        name = 'Attach remote',
        connect = {
            host = "127.0.0.1",
            port = 5678
        },
    }
}
