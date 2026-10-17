return {
  {
    'nvim-telescope/telescope.nvim',
    version = '*',
    dependencies = {
      'nvim-lua/plenary.nvim',
      { 'nvim-telescope/telescope-fzf-native.nvim', build = 'make' },
    }
  },
  {
    -- the main branch is the rewrite for nvim 0.11+; parsers need the tree-sitter CLI
    "nvim-treesitter/nvim-treesitter",
    branch = "main",
    lazy = false,
    build = ":TSUpdate",
    config = function()
      require("nvim-treesitter").install({
        "c", "lua", "javascript", "typescript", "tsx", "python", "rust", "go", "bash",
        "json", "yaml", "toml", "html", "css", "markdown", "markdown_inline", "vim", "vimdoc", "query",
      })
      vim.api.nvim_create_autocmd("FileType", {
        callback = function(ev)
          if pcall(vim.treesitter.start, ev.buf) then
            vim.bo[ev.buf].indentexpr = "v:lua.require'nvim-treesitter'.indentexpr()"
          end
        end,
      })
    end,
  },
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      "nvim-tree/nvim-web-devicons",
    },
    lazy = false,
    opts = {
      close_if_last_window = true,
      popup_border_style = "rounded",
      default_component_configs = {
        indent = { with_markers = true, indent_marker = "│", last_indent_marker = "└" },
        icon = { folder_closed = "\u{f07b}", folder_open = "\u{f07c}", folder_empty = "\u{f114}" },
        git_status = { symbols = { added = "+", modified = "◆", deleted = "✖", untracked = "◇" } },
      },
      window = { width = 32 },
      filesystem = { follow_current_file = { enabled = true } },
    },
  },
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    opts = {
      options = {
        theme = "attack-on-titan",
        component_separators = { left = "\u{e0b9}", right = "\u{e0bb}" },
        section_separators = { left = "\u{e0b8}", right = "\u{e0be}" },
        globalstatus = true,
        disabled_filetypes = { statusline = { "alpha" } },
      },
      sections = {
        lualine_a = { { "mode", icon = "◆" } },
        lualine_b = { "branch", "diff" },
        lualine_c = { { "filename", path = 1, symbols = { modified = " ●", readonly = " \u{f023}" } } },
        lualine_x = { "diagnostics", "filetype" },
        lualine_y = { "progress" },
        lualine_z = { "location" },
      },
    },
  },
  {
    "akinsho/bufferline.nvim",
    version = "*",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    event = "VeryLazy",
    opts = function()
      local c = require("aot").palette
      return {
        options = {
          separator_style = "slant",
          always_show_bufferline = false,
          diagnostics = "nvim_lsp",
          show_close_icon = false,
          offsets = { { filetype = "neo-tree", text = "\u{25c6} Survey Corps", highlight = "NeoTreeRootName" } },
        },
        highlights = {
          fill = { bg = c.abyss },
          background = { fg = c.muted, bg = c.bg1 },
          buffer_selected = { fg = c.fg_hi, bg = c.bg, bold = true, italic = false },
          separator = { fg = c.abyss, bg = c.bg1 },
          separator_selected = { fg = c.abyss, bg = c.bg },
          separator_visible = { fg = c.abyss, bg = c.bg1 },
          indicator_selected = { fg = c.crimson, bg = c.bg },
          modified_selected = { fg = c.brass, bg = c.bg },
          close_button_selected = { fg = c.red, bg = c.bg },
        },
      }
    end,
  },
  {
    "goolord/alpha-nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      local alpha = require("alpha")
      local dash = require("alpha.themes.dashboard")
      local wings = require("aot.wings")
      dash.section.header = {
        type = "group",
        val = {
          { type = "text", val = wings.lines, opts = { position = "center", hl = wings.hl } },
          { type = "padding", val = 1 },
          { type = "text", val = "S H I N Z O U   W O   S A S A G E Y O", opts = { position = "center", hl = "AlphaMotto" } },
        },
      }
      local function btn(key, icon, label, cmd)
        local b = dash.button(key, icon .. "  " .. label, cmd)
        b.opts.hl = "AlphaButtons"
        b.opts.hl_shortcut = "AlphaShortcut"
        return b
      end
      dash.section.buttons.val = {
        btn("f", "\u{f002}", "Find file", "<cmd>Telescope find_files<CR>"),
        btn("r", "\u{f1da}", "Recent files", "<cmd>Telescope oldfiles<CR>"),
        btn("g", "\u{f15c}", "Grep", "<cmd>Telescope live_grep<CR>"),
        btn("e", "\u{f15b}", "New file", "<cmd>ene<CR>"),
        btn("c", "\u{f013}", "Config", "<cmd>e $MYVIMRC<CR>"),
        btn("l", "󰒲", "Lazy", "<cmd>Lazy<CR>"),
        btn("q", "\u{f011}", "Quit", "<cmd>qa<CR>"),
      }
      local quotes = {
        "If you win, you live. If you lose, you die. If you don't fight, you can't win.",
        "The world is cruel, but also very beautiful.",
        "Give up on your dreams and die.",
        "I'll keep moving forward until my enemies are destroyed.",
        "Dedicate your heart.",
      }
      math.randomseed(os.time())
      dash.section.footer.val = "— " .. quotes[math.random(#quotes)]
      dash.section.footer.opts.hl = "AlphaFooter"
      dash.config.layout = {
        { type = "padding", val = 1 },
        dash.section.header,
        { type = "padding", val = 2 },
        dash.section.buttons,
        { type = "padding", val = 1 },
        dash.section.footer,
      }
      alpha.setup(dash.config)
    end,
  },
  { "lewis6991/gitsigns.nvim", event = "BufReadPre", opts = { current_line_blame = false } },
  {
    "folke/which-key.nvim",
    event = "VeryLazy",
    opts = { preset = "modern", win = { border = "rounded" } },
  },
  {
    "lukas-reineke/indent-blankline.nvim",
    main = "ibl",
    event = "BufReadPost",
    opts = { indent = { char = "│" }, scope = { enabled = true, show_start = false, show_end = false } },
  },
  { "windwp/nvim-autopairs", event = "InsertEnter", opts = {} },
}
