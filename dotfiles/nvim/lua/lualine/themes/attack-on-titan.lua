local c = require("aot").palette

return {
  normal = {
    a = { fg = c.fg_hi, bg = c.crimson, gui = "bold" },
    b = { fg = c.fg, bg = c.bg3 },
    c = { fg = c.fg_dim, bg = c.bg1 },
  },
  insert = { a = { fg = c.abyss, bg = c.moss, gui = "bold" }, b = { fg = c.fg, bg = c.bg3 } },
  visual = { a = { fg = c.abyss, bg = c.brass, gui = "bold" }, b = { fg = c.fg, bg = c.bg3 } },
  replace = { a = { fg = c.abyss, bg = c.steam, gui = "bold" }, b = { fg = c.fg, bg = c.bg3 } },
  command = { a = { fg = c.abyss, bg = c.sky, gui = "bold" }, b = { fg = c.fg, bg = c.bg3 } },
  terminal = { a = { fg = c.abyss, bg = c.teal, gui = "bold" }, b = { fg = c.fg, bg = c.bg3 } },
  inactive = {
    a = { fg = c.muted, bg = c.bg1 },
    b = { fg = c.muted, bg = c.bg1 },
    c = { fg = c.muted, bg = c.bg1 },
  },
}
