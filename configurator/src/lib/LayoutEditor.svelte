<script>
  import { db, loadLayout } from "./db";
  import { liveQuery } from "dexie";
  import { currentKey, currentLayout, conversion } from "./stores";

  let currentRowIdx;
  let currentColIdx;
  async function getNextKey() {
    //Check if we're skipping to the next row
    currentColIdx++;
    if (currentColIdx > $currentLayout.keys[currentRowIdx].length - 1) {
      currentColIdx = 0;
      currentRowIdx++;
    }

    //if overflow of the row idx skip back to 0
    if (currentRowIdx > $currentLayout.keys.length - 1) {
      currentRowIdx = 0;
    }

    setTimeout(() => {
      $currentKey = $currentLayout.keys[currentRowIdx][currentColIdx];
    }, 200);
  }
  async function onKeyClick(key, rowIdx, colIdx) {
    $currentKey = key;
    currentRowIdx = rowIdx;
    currentColIdx = colIdx;
  }
  async function mapKeyFromMap(event) {
    let modifier = await getModifier();
    let foundKey = $conversion.filter((key) => {
      return key.js?.[modifier]?.key.toLowerCase() === event.key.toLowerCase();
    });

    //flatten the shit out of this
    if (foundKey[0]) {
      $currentKey.key = foundKey[0].js?.[modifier]?.key;
      $currentKey.code = foundKey[0].js?.[modifier]?.code;
      $currentKey.keyCode = foundKey[0].js?.[modifier]?.keyCode;
      $currentKey.usbHidCode = foundKey[0].usbHidCode;
      $currentKey.qmk = foundKey[0].qmk;
      $currentKey.desc = foundKey[0].desc;
      $currentKey.modifier = modifier;
      await getNextKey();
    }
  }
  async function getModifier() {
    if (modKeys.shift) {
      return "shift";
    }
    if (modKeys.altGr) {
      return "altGr";
    }
    if (modKeys.alt) {
      return "alt";
    }
    if (modKeys.ctrl) {
      return "ctrl";
    }
    return "none";
  }

  let modKeys = {};
  async function onKeyRelease(event) {
    event.preventDefault();
    if (event.key === "Shift") {
      modKeys.shift = false;
    } else if (event.key === "Alt") {
      modKeys.alt = false;
    } else if (event.key === "Control") {
      modKeys.ctrl = false;
    } else if (event.key === "AltGraph") {
      modKeys.altGr = false;
    }

    //if no key registered, assume the modifier is the key
    if ($currentKey.key === undefined) {
      await mapKeyFromMap(event);
    }
  }
  async function onKeyPress(event) {
    //Figure out if a modifier is pressed
    //let modifier = "none";
    event.preventDefault();

    if (event.key === "Shift") {
      modKeys.shift = true;
    } else if (event.key === "Alt") {
      modKeys.alt = true;
    } else if (event.key === "Control") {
      modKeys.ctrl = true;
    } else if (event.key === "AltGraph") {
      modKeys.altGr = true;
    } else {
      await mapKeyFromMap(event);
    }
  }
</script>

<div class="layout">
  {#if $currentLayout}
    {#each $currentLayout.keys as row, rowIdx}
      <div class="row">
        {#each row as key, colIdx}
          <!-- svelte-ignore a11y_no_static_element_interactions -->
          <button
            class="key width-{('' + key.width).replace('.', '')}u {key ===
            $currentKey
              ? 'current'
              : ''} "
            on:click={() => onKeyClick(key, rowIdx, colIdx)}
            on:keydown={onKeyPress}
            on:keyup={onKeyRelease}
          >
            {key.key}
          </button>
        {/each}
      </div>
    {/each}
  {/if}
</div>

<style>
  .key {
    display: inline-block;
    height: 64px;
    border: 1px solid white;
    border-radius: 2px;
    width: 64px;
    margin: 1px;
    overflow: hidden;
    padding: 0px;
  }
  .width-05u {
    width: 31px;
  }
  .width-075u {
    width: 47.5px;
  }
  .width-1u {
    width: 64px;
  }
  .width-2u {
    width: 128px;
  }
  .width-3u {
    width: 196px;
  }
  .width-4u {
    width: 266px;
  }
  .width-5u {
    width: 328px;
  }
  .width-6u {
    width: 400px;
  }
  .width-7u {
    width: 468px;
  }
  .row {
    display: flex;
    flex-direction: row;
    place-items: center;
  }
  .layout {
    width: 70%;
  }
  .current {
    border-color: blue;
  }
</style>
