<script>
  import LayoutEditor from "./lib/LayoutEditor.svelte";
  import Settings from "./lib/Settings.svelte";
  let pageName = "main";
  let keyboardId = 0;
</script>

<main>
  <!--- Dropdown here-->
  {#if keyboardId == 0}
    <Settings></Settings>
  {:else}
    <LayoutEditor></LayoutEditor>
  {/if}
</main>
