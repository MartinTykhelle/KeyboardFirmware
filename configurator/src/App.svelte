<script>
  import LayoutEditor from './lib/LayoutEditor.svelte';
  import Settings from './lib/Settings.svelte';
  import { db, loadLayout } from './lib/db';
  import { currentLayoutId, currentLayerId, currentKey, currentLayout, conversion, currentLayer } from './lib/stores';
  import { liveQuery } from 'dexie';
  import conv from './lib/conversion.json';

  let settings = $state();
  $currentLayoutId = 0;
  $currentLayerId = 0;
  $currentKey = undefined;
  $conversion = conv.keys;

  let keyboardLayouts = liveQuery(() => db.table('layout').toArray());
  async function refreshLayout() {
    $currentLayout = await loadLayout($currentLayoutId);
    $currentLayer = $currentLayout.layers[$currentLayerId];
    console.log($currentLayer);
    $currentKey = undefined;
  }
  //sidebar component
  let widths = [0.5, 0.75, 1, 2, 3, 4, 5, 6, 7];

  async function onWidth() {
    $currentLayout = $currentLayout;
    $currentLayer = $currentLayer;
  }
</script>

<main>
  <div class="container">
    <div class="sidebar">
      Layout:
      <select bind:value={$currentLayoutId} onchange={refreshLayout}>
        <option value={0} selected> New</option>
        {#each $keyboardLayouts || [] as layout (layout.layoutId)}
          <option value={layout.layoutId}> {layout.layoutName}</option>
        {/each}
      </select>
      <div>
        {#if $currentLayoutId}
          Layer:
          <select bind:value={$currentLayerId} onchange={refreshLayout}>
            {#each $currentLayout.layers as layer, layerIdx}
              <option value={layerIdx}> {layerIdx}</option>
            {/each}
          </select>
        {/if}

        {#if $currentKey}
          <!---- Component this shizzle-->

          <div>
            <!--- Width should be moved from key to a new array so it's propagated through the layers-->
            Width:
            <select bind:value={$currentKey.width} onchange={onWidth}>
              {#each widths as width}
                <option value={width}>{width}</option>
              {/each}
            </select>
          </div>
          <div>Desc: {$currentKey.desc}</div>
          <div>Key: {$currentKey?.key}</div>
          <div>Code: {$currentKey?.code}</div>
          <div>KeyCode: {$currentKey?.keyCode}</div>
          <div>HID:{$currentKey?.usbHidCode}</div>
          <div>QMK:{$currentKey?.qmk}</div>
          <div>Modifier:{$currentKey?.modifier}</div>
          <!--- Delete key-->
          <!--- Null out key-->
        {/if}
      </div>
    </div>
    {#if !$currentLayoutId}
      <Settings bind:this={settings}></Settings>
    {:else}
      <LayoutEditor></LayoutEditor>
    {/if}
  </div>
</main>

<style>
  .container {
    display: flex;
    flex-direction: row;
  }
  .sidebar {
    width: 30%;
  }
</style>
