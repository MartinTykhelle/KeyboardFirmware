<script>
  import {
    currentLayoutId,
    currentLayerId,
    currentKey,
    currentLayout,
    currentLayer,
    conversion,
    currentRowIdx,
    currentColIdx,
  } from "./stores";
  import { db, saveLayout, loadLayout } from "./db.js";
  import { liveQuery } from "dexie";

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
    await saveLayout($currentLayout.layoutId, $currentLayout);
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
  async function deleteKey() {
    console.log($currentLayout);
  }
  async function unsetKey() {
    //$currentKey = { lowerKey: $currentKey.lowerKey };
    console.log($currentLayout);
    //await saveLayout($currentLayout.layoutId, $currentLayout);
  }
</script>

<table>
  <tbody>
    <tr>
      <td>Layout</td>
      <td>
        <select bind:value={$currentLayoutId} onchange={refreshLayout}>
          <option value={0} selected> New</option>
          {#each $keyboardLayouts || [] as layout (layout.layoutId)}
            <option value={layout.layoutId}> {layout.layoutName}</option>
          {/each}
        </select>
      </td>
    </tr>
    {#if $currentLayoutId > 0 && $currentLayout}
      <tr>
        <td>Layer</td>
        <td>
          <select bind:value={$currentLayerId}>
            {#each $currentLayout.layers as layer, layerIdx}
              <option value={layerIdx}> {layerIdx}</option>
            {/each}
          </select>
        </td>
      </tr>
    {/if}
    {#if $currentKey}
      <tr>
        <td>Width</td>
        <td>
          <select
            bind:value={
              $currentLayout.layout[$currentRowIdx][$currentColIdx].width
            }
            onchange={onWidth}
          >
            {#each widths as width}
              <option value={width}>{width}</option>
            {/each}
          </select>
        </td>
      </tr>
      {#if $currentKey.usesLower}
        <tr>
          <td colspan="2">Key from lower layer</td>
        </tr>
        <tr>
          <td>Desc</td>
          <td>{$currentKey.lowerKey.desc}</td>
        </tr>
      {:else}
        <tr>
          <td>Desc</td>
          <td>{$currentKey.desc}</td>
        </tr>
        <tr>
          <td>Key</td>
          <td>{$currentKey?.key}</td>
        </tr>
        <tr>
          <td>Code</td>
          <td>{$currentKey?.code}</td>
        </tr>
        <tr>
          <td>KeyCode</td>
          <td>{$currentKey?.keyCode}</td>
        </tr>
        <tr>
          <td>HID</td>
          <td>{$currentKey?.usbHidCode}</td>
        </tr>
        <tr>
          <td>QMK</td>
          <td>{$currentKey?.qmk}</td>
        </tr>
        <tr>
          <td>Modifier</td>
          <td>{$currentKey?.modifier}</td>
        </tr>
        <tr>
          <td>Manual</td>
          <td>
            <select bind:value={modifier}>
              {#each modifiers as mod}
                <option value={mod.r}>{mod.d}</option>
              {/each}
            </select>
          </td>
        </tr>
        <tr>
          <td></td>
          <td>
            <select bind:value={convIdx} onchange={setCurrentKey}>
              {#each $conversion as conv, idx}
                <option value={idx}>{conv.desc}</option>
              {/each}
            </select>
          </td>
        </tr>
      {/if}
      <tr>
        <td colspan="2"><button onclick={deleteKey}>Delete Key</button></td>
      </tr>
      <tr>
        <td colspan="2"><button onclick={unsetKey}>Unset Key</button></td>
      </tr>
    {/if}
  </tbody>
</table>

<!--  Delete should delete both the element in the new array and in the layer-->
<!-- layer modifiers should also be part of the outside array as they propagate all layers-->
<!-- hold / tap logic maybe too-->

<style>
  select {
    width: 96%;
  }

  table {
    width: 100%;
  }
  td:nth-child(1) {
    width: 30%;
  }
</style>
