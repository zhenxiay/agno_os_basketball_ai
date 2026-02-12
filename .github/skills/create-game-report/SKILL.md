---
name: create-game-report
description: Guide for AI agent to create game report of a selected NBA game.
---

# Game Report Skill Guide

## Overview

This file is a guide for AI agent to create game report of a selected NBA game.

---

## Workflow

1. Ask user for necessary inputs:
   - date
   - home_team
   - away_team

   If user needs help for some of the input parameters, run following command to get help:
   ```
   uv run scripts/get_game_data.py --help
   ```

2. Run following command to get the play-to-play data of the selected game:

   ```
   uv run scripts/get_game_data.py
   ```    
   
   The output data (in TOON format) is to be loaded to agent's context for the next step.

3. Create game report based on the data retrieved from previous step.

   Describe the game like a game report in the newspaper.
   Include the following information in the report:
        
    - Game summary
    - Game highlights
    - Game statistics

    Format the response using markdown and include tables where appropriate.

## Error handling

**Script cannot be found**: If the Agent gets this error, use `powershell`commands to search for the script on the local machine.

**Parameters missing or incorrect**: If the Agent gets error regarding any missing or incorrect input parameters, repeat *step 1* and confirm with user.