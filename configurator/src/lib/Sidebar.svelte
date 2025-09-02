<script>
  import {
    currentLayoutId,
    currentLayerId,
    currentKey,
    currentLayout,
    currentLayer,
    conversion,
  } from "./stores";
  import { db, saveLayout, loadLayout } from "./db.js";
  import { liveQuery } from "dexie";
  import AttrPair from "./AttrPair.svelte";

  let keyboardLayouts = liveQuery(() => db.table("layout").toArray());
  //sidebar component
  let widths = [0.5, 0.75, 1, 2, 3, 4, 5, 6, 7];
  let modifiers = [
    { d: "None", r: "none" },
    { d: "Shift", r: "shift" },
    { d: "Control", r: "altGr" },
    { d: "Alt", r: "alt" },
    { d: "Control", r: "ctrl" },
  ];
  let modifier = "none";
  let convIdx;
  async function onWidth() {
    $currentLayout = $currentLayout;
    $currentLayer = $currentLayer;
  }

  async function setCurrentKey() {
    $currentKey.key = $conversion[convIdx].js?.[modifier]?.key;
    $currentKey.code = $conversion[convIdx].js?.[modifier]?.code;
    $currentKey.keyCode = $conversion[convIdx].js?.[modifier]?.keyCode;
    $currentKey.usbHidCode = $conversion[convIdx].usbHidCode;
    $currentKey.qmk = $conversion[convIdx].qmk;
    $currentKey.desc = $conversion[convIdx].desc;
    await saveLayout($currentLayout.layoutId, $currentLayout);
  }

  function getLowerKey(key, rowIdx, colIdx) {
    let returnKey = {
      key: key.key,
      code: key.code,
      keyCode: key.keyCode,
      usbHidCode: key.usbHidCode,
      qmk: key.qmk,
      desc: key.desc,
      modifier: key.modifier,
    };
    if (typeof key.key == "undefined") {
      for (let index = $currentLayerId - 1; index >= 0; index--) {
        let lowerLevelKey = $currentLayout.layers[index][rowIdx][colIdx];
        console.log(index, $currentLayout.layers[index][rowIdx][colIdx]);
        if (lowerLevelKey.key) {
          console.log("found " + lowerLevelKey);
          returnKey = {
            key: lowerLevelKey.key,
            code: lowerLevelKey.code,
            keyCode: lowerLevelKey.keyCode,
            usbHidCode: lowerLevelKey.usbHidCode,
            qmk: lowerLevelKey.qmk,
            desc: lowerLevelKey.desc,
            modifier: lowerLevelKey.modifier,
          };
          key.usesLower = true;
          break;
        }
      }
    }
    return returnKey;
  }
  $: refreshLayout({ layer: $currentLayerId, layout: $currentLayoutId });

  async function refreshLayout(ids) {
    if (ids.layout) {
      $currentLayout = await loadLayout(ids.layout);
      $currentLayer = $currentLayout.layers[ids.layer];

      //populate lower keys, used for transparent keys
      for (let rowIdx = 0; rowIdx < $currentLayer.length; rowIdx++) {
        for (let colIdx = 0; colIdx < $currentLayer[rowIdx].length; colIdx++) {
          $currentLayer[rowIdx][colIdx].lowerKey = getLowerKey(
            $currentLayer[rowIdx][colIdx],
            rowIdx,
            colIdx
          );
        }
      }
    }
    $currentKey = undefined;
  }
</script>

<div>
  <AttrPair>
    <span slot="label">Layout</span>
    <span slot="content">
      <select bind:value={$currentLayoutId} onchange={refreshLayout}>
        <option value={0} selected> New</option>
        {#each $keyboardLayouts || [] as layout (layout.layoutId)}
          <option value={layout.layoutId}> {layout.layoutName}</option>
        {/each}
      </select>
    </span>
  </AttrPair>
  {#if $currentLayoutId > 0 && $currentLayout}
    <AttrPair>
      <span slot="label">Layer</span>
      <span slot="content">
        <select bind:value={$currentLayerId}>
          {#each $currentLayout.layers as layer, layerIdx}
            <option value={layerIdx}> {layerIdx}</option>
          {/each}
        </select>
      </span>
    </AttrPair>
  {/if}

  {#if $currentKey}
    <div>
      <!--- Width should be moved from key to a new array so it's propagated through the layers-->
      <!--  Delete should delete both the element in the new array and in the layer-->
      <!-- layer modifiers should also be part of the outside array as they propagate all layers-->
      <!-- hold / tap logic maybe too-->

      <AttrPair>
        <span slot="label"> Width</span>
        <span slot="content">
          <select bind:value={$currentKey.width} onchange={onWidth}>
            {#each widths as width}
              <option value={width}>{width}</option>
            {/each}
          </select>
        </span>
      </AttrPair>
    </div>
    <!-- This should be some sort of grid probably-->

    {#if $currentKey.usesLower}
      <AttrPair>
        <span slot="label">Key from lower layer</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">Desc</span>
        <span slot="content">{$currentKey.lowerKey.desc}</span>
      </AttrPair>
    {:else}
      <AttrPair>
        <span slot="label">Desc</span>
        <span slot="content">{$currentKey.desc}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">Key</span>
        <span slot="content">{$currentKey?.key}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">Code</span>
        <span slot="content">{$currentKey?.code}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">KeyCode</span>
        <span slot="content">{$currentKey?.keyCode}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">HID</span>
        <span slot="content">{$currentKey?.usbHidCode}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">QMK</span>
        <span slot="content">{$currentKey?.qmk}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label">Modifier</span>
        <span slot="content">{$currentKey?.modifier}</span>
      </AttrPair>
      <AttrPair>
        <span slot="label"> Manual</span>
        <span slot="content">
          <select bind:value={modifier}>
            {#each modifiers as mod}
              <option value={mod.r}>{mod.d}</option>
            {/each}
          </select>
          <select bind:value={convIdx} onchange={setCurrentKey}>
            {#each $conversion as conv, idx}
              <option value={idx}>{conv.desc}</option>
            {/each}
          </select>
        </span>
      </AttrPair>
    {/if}
    <!--- Delete key-->
    <!--- Null out key-->
  {/if}
</div>

<style>
  select {
    width: 80%;
  }
</style>
