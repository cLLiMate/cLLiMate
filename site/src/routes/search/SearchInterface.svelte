<script>
  import pDebounce from "p-debounce";
  import { build_path } from "$lib/api.js";
  import Table from "$lib/Table.svelte";

  async function search(text) {
    console.log("searching for", text);
    let url = build_path(import.meta.env.VITE_API_HOST, "articles/search", true);
    let resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });
    let data = await resp.json();
    return data;
  }

  let text = null;
  let data;
  let debouncedSearch = pDebounce((text) => {
    search(text).then((res) => {
      data = res;
    });
  }, 500);
  $: text && debouncedSearch(text);

  $: options = {
    autoColumns: true,
    autoColumnsDefinitions: [{ field: "embedding", visible: false }]
  };
</script>

<div class="searchbar">
  <input type="text" bind:value={text} placeholder="ocean acidification" />
</div>

{#if data}
  <Table {data} {options} />
{/if}

<style>
  .searchbar {
    display: flex;
    justify-content: center;
    margin: 1rem;
  }
  .searchbar input {
    width: 100%;
    padding: 0.5rem;
    font-size: 1.5rem;
  }
</style>
