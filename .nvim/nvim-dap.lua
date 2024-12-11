local dap = require("dap")

dap.adapters.lldb = {
    type = "executable",
    command = "/usr/bin/lldb-vscode-14", -- adjust as needed
    name = "lldb",
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
