<script>
  import LayoutEditor from "./lib/LayoutEditor.svelte";
  import Settings from "./lib/Settings.svelte";
  import {
    currentLayoutId,
    currentLayerId,
    currentKey,
    conversion,
  } from "./lib/stores";
  import conv from "./lib/conversion.json";
  import Sidebar from "./lib/Sidebar.svelte";

  $currentLayoutId = 0;
  $currentLayerId = 0;
  $currentKey = undefined;
  $conversion = conv.keys;
</script>

<main>
  <div class="container">
    <div class="sidebar">
      <Sidebar></Sidebar>
    </div>
    {#if !$currentLayoutId}
      <Settings></Settings>
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
