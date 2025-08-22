<script>
  import LayoutEditor from "./lib/LayoutEditor.svelte";
  import Settings from "./lib/Settings.svelte";
  import { db } from "./lib/db";
  import { currentLayoutId } from "./lib/stores";
  import { liveQuery } from "dexie";

  let settings = $state();
  $currentLayoutId = 0;

  let keyboardLayouts = liveQuery(() => db.table("layout").toArray());
</script>

<main>
  <!--- Dropdown here-->
  Layout:
  <select bind:value={$currentLayoutId}>
    <option value={0} selected> New</option>
    {#each $keyboardLayouts || [] as layout (layout.layoutId)}
      <option value={layout.layoutId}> {layout.layoutName}</option>
    {/each}
  </select>
  {#if !$currentLayoutId || $currentLayoutId == "0"}
    <Settings bind:this={settings}></Settings>
  {:else}
    <LayoutEditor></LayoutEditor>
  {/if}
</main>
