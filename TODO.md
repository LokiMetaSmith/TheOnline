# Project Expansion TODO List

## Phase 1: World Expansion (The Whispering Vale)
Create a rich starting area to provide context for the LLM characters.

- [ ] **Create Batch Build File (`world/build.ev`)**
    - [ ] **The Village of Oakhaven**:
        - [ ] *Town Square*: The central hub.
        - [ ] *The Rusty Tankard (Inn)*: A place for social interaction.
        - [ ] *Blacksmith's Forge*: Demonstrates crafting/items.
        - [ ] *General Store*: Trading hub.
    - [ ] **The Whispering Woods**:
        - [ ] Connected to the village.
        - [ ] Dangerous area for "High Autonomy" testing.
    - [ ] **The Ruined Watchtower**:
        - [ ] A location with lore and potential puzzles.

- [ ] **Populate with Unique NPCs**
    - [ ] **Barnaby (Innkeeper)**: Friendly, gossip-prone. Knows about town events.
    - [ ] **Kaelen (Blacksmith)**: Grumpy, focused on work. Wants specific materials.
    - [ ] **Elara (Mystic)**: Lives in the woods/tower. High autonomy, speaks in riddles.

## Phase 2: Enhanced Interactivity (Code)
Update `LLMCharacter` to be more aware and reactive.

- [ ] **Sensory Perception (`typeclasses/llm_character.py`)**
    - [ ] Update `at_tick` prompt to include a list of **visible objects** and **other characters** in the room.
        - *Current*: "You are in {location}."
        - *Goal*: "You are in {location}. You see: {list_of_objects}. {list_of_chars} are here."
    - [ ] Allow LLM to act on these (e.g., "look at <char>", "get <item>").

- [ ] **Event Reactivity**
    - [ ] Implement `at_object_receive(self, obj, source)`:
        - When an item is given to the NPC, trigger an LLM response/evaluation.
        - "Thank you for the {obj.key}!" or "I don't need this."
    - [ ] Implement `at_char_enter(self, char)` (via room hook or custom script):
        - NPC acknowledges players entering the room.

- [ ] **Memory & Context**
    - [ ] Implement `summarize_memory()`:
        - If `chat_history` gets too long, ask LLM to summarize key facts and store them in `permanent_memory`, then clear detailed history.

## Phase 3: Advanced Mechanics
Features that make the game a "game".

- [ ] **Goal-Oriented Behavior**
    - [ ] Give NPCs a `goal` attribute (e.g., "Collect 3 apples", "Protect the gate").
    - [ ] Inject the goal into the System Prompt.

- [ ] **Roaming**
    - [ ] Enable NPCs to move between rooms logically (pathfinding or random walk with intent).

- [ ] **Dynamic Description**
    - [ ] Allow the LLM to update its own Description (`desc`) based on its state/health/inventory.
