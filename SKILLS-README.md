# Skills powered by coderunner, running locally on your Mac

> [!NOTE]
> [CodeRunner](https://github.com/instavm/coderunner) executes AI-generated code in a truly isolated sandboxed environment on your Mac using Apple's native containers.

# Pre-requisite
* `Mac` with a `M-series` chip.
* Install the latest`coderunner` by running the `./install.sh` script from the main repository.
```shell
./install.sh
```

# How To Use Skills
* `coderunner` is exposed as an MCP and can be connected to tools like `gemini cli` or `qwen cli` or `claude desktop` or anything that supports MCP. The execution is completely local, done on your Mac.

*For example, for Gemini CLI, you can edit* `~/.gemini/settings.json`
  ```json
  {
  "theme": "Default",
  "selectedAuthType": "oauth-personal",
  "mcpServers": {
    "coderunner": {
      "httpUrl": "http://coderunner.local:8222/mcp"
    }
  }
}
```



# How To Add New Skills

## Option 1: Import from Claude

You can either download and copy the folder from Anthropic skills's [github repo](https://github.com/anthropics/skills/) to `~/.coderunner/assets/skills/user/<new-skill-folder>`

For example, I have added 4 skills in the user folder as:
```shell
/Users/manish/.coderunner/assets/skills/
├── public
│   ├── image-crop-rotate
│   │   ├── scripts
│   │   └── SKILL.md
│   └── pdf-text-replace
│       ├── scripts
│       └── SKILL.md
└── user
    ├── docx
    │   ├── docx-js.md
    │   ├── LICENSE.txt
    │   ├── ooxml
    │   ├── ooxml.md
    │   ├── scripts
    │   └── SKILL.md
    ├── pptx
    │   ├── html2pptx.md
    │   ├── LICENSE.txt
    │   ├── ooxml
    │   ├── ooxml.md
    │   ├── scripts
    │   └── SKILL.md
    ├── slack-gif-creator
    │   ├── core
    │   ├── LICENSE.txt
    │   ├── requirements.txt
    │   ├── SKILL.md
    │   └── templates
    └── xlsx
        ├── LICENSE.txt
        ├── recalc.py
        └── SKILL.md
```


## Option 2: Write Your Own Skills

* You can create a folder in the similar structure as above, where only mandatory file is the `SKILL.md`. [Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
* You can also ask claude to generate one like `Can you write a skill which creates ascii art of words given one.`
  After it creates the skill, it will let you download a `ZIP` file which you can place directly (no need to expand) in `~/.coderunner/assets/skills/user`

Test drive with Gemini CLI

```
> /mcp

Configured MCP servers:

🟢 coderunner - Ready (5 tools)
  Tools:
  - execute_python_code
  - get_skill_file
  - get_skill_info
  - list_skills
  - navigate_and_get_all_visible_text

> can you generate ascii art for "CODERUNNER"

✦ I will generate the ASCII art you desire. First, I must survey my available skills.
✓  list_skills (coderunner MCP Server)

✦ I have located a relevant skill: ascii-art. I will now retrieve its instructions.
✓  get_skill_info (coderunner MCP Server) {"skill_name":"ascii-art"}
✦ Your ASCII art is ready:

   1   ____ ___  ____  _____ ____  _   _ _   _ _   _ _____ ____
   2  / ___/ _ \|  _ \| ____|  _ \| | | | \ | | \ | | ____|  _ \
   3 | |  | | | | | | |  _| | |_) | | | |  \| |  \| |  _| | |_) |
   4 | |__| |_| | |_| | |___|  _ <| |_| | |\\  | |\\  | |___|  _ <
   5  \____\___/|____/|_____|_| \_\\___/|_| \_|_| \_|_____|_| \_\
   6




Using: 1 GEMINI.md file | 3 MCP servers (ctrl+t to view)
```
