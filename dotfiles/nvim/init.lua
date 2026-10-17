-- Shinzou wo Sasageyo
vim.cmd("set expandtab")
vim.cmd("set tabstop=2")
vim.cmd("set softtabstop=2")
vim.cmd("set shiftwidth=2")
vim.g.mapleader = " "

vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.cursorline = true
vim.opt.signcolumn = "yes"
vim.opt.termguicolors = true
vim.opt.scrolloff = 8
vim.opt.smartcase = true
vim.opt.ignorecase = true
vim.opt.splitright = true
vim.opt.splitbelow = true
vim.opt.updatetime = 250
vim.opt.undofile = true
vim.opt.showmode = false
vim.opt.clipboard = "unnamedplus"
vim.opt.fillchars = { eob = " ", fold = " ", vert = "│" }
vim.opt.pumheight = 12

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end

vim.api.nvim_create_autocmd("BufEnter", {
  pattern = "*",
  command = "silent! lcd %:p:h",
})

-- flash the yanked text in brass
vim.api.nvim_create_autocmd("TextYankPost", {
  callback = function() vim.hl.on_yank({ higroup = "Search", timeout = 180 }) end,
})

vim.opt.rtp:prepend(lazypath)

require("lazy").setup("plugins", {
  install = { colorscheme = { "attack-on-titan" } },
  ui = { border = "rounded", title = " Survey Corps " },
  change_detection = { notify = false },
})

vim.cmd.colorscheme("attack-on-titan")

local builtin = require("telescope.builtin")
vim.keymap.set('n', '<C-p>', builtin.find_files, { desc = "Find files" })
vim.keymap.set('n', '<leader>fg', builtin.live_grep, { desc = "Live grep" })
vim.keymap.set('n', '<leader>fb', builtin.buffers, { desc = "Buffers" })
vim.keymap.set('n', '<leader>fr', builtin.oldfiles, { desc = "Recent files" })
vim.keymap.set('n', '<C-n>', ":Neotree filesystem reveal left<CR>", { desc = "File tree" })
vim.keymap.set('n', '<S-l>', "<cmd>BufferLineCycleNext<CR>", { desc = "Next buffer" })
vim.keymap.set('n', '<S-h>', "<cmd>BufferLineCyclePrev<CR>", { desc = "Previous buffer" })
vim.keymap.set('n', '<leader>w', "<cmd>w<CR>", { desc = "Save" })
vim.keymap.set('n', '<Esc>', "<cmd>nohlsearch<CR>")

require("telescope").setup({
  defaults = {
    layout_strategy = "horizontal",
    layout_config = {
      width = 0.9,
      height = 0.9,
      preview_width = 0.6,
    },
    prompt_prefix = " \u{f002}  ",
    selection_caret = "◆ ",
    borderchars = { " ", " ", " ", " ", " ", " ", " ", " " },
  },
})
pcall(require("telescope").load_extension, "fzf")
