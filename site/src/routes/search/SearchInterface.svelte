<script>
  import pDebounce from "p-debounce";
  import { build_path } from "$lib/api.js";
  import Table from "$lib/Table.svelte";
  import { DoubleBounce } from "svelte-loading-spinners";

  let text = null;
  let data;
  let loaded = false;

  async function search(text) {
    let url = build_path(import.meta.env.VITE_API_HOST, "articles/search", true);
    let resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });
    return await resp.json();
  }

  async function testReadyForSearch() {
    // We have to load the glove embedding on the backend, which takes 10-20 second on cold start.
    // We check on this and add a loading indicator until it's ready.
    await search("test query");

    // set loaded to true to enable the search bar
    loaded = true;
  }

  let debouncedSearch = pDebounce((text) => {
    search(text).then((res) => {
      data = res;
    });
  }, 500);
  $: text && debouncedSearch(text);

  $: options = {
    autoColumns: true,
    autoColumnsDefinitions: [
      { field: "embedding", visible: false },
      { field: "headline", formatter: "link", formatterParams: { urlField: "url" } },
      { field: "url", visible: false },
      { field: "sentiment_score", formatter: (cell) => cell.getValue().toFixed(4) }
    ]
  };
</script>

<div class="searchbar">
  <input type="text" bind:value={text} placeholder="ocean acidification" disabled={!loaded} />
</div>

{#await testReadyForSearch()}
  <div class="loading">
    <DoubleBounce size="120" />
  </div>
{:then}
  {#if data}
    <Table {data} {options} />
  {/if}
{/await}

<style>
  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 300px;
  }
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
