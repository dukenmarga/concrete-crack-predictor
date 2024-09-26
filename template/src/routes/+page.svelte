<script lang="ts">
    import { Button } from "$lib/components/ui/button/index";
    import * as Card from "$lib/components/ui/card/index";
    import { Input } from "$lib/components/ui/input/index";
    import { Label } from "$lib/components/ui/label";
    import Reload from "svelte-radix/Reload.svelte";
    import { Separator } from "$lib/components/ui/separator/index.js";

    import * as Tabs from "$lib/components/ui/tabs/index.js";
    
    let content: string | undefined = undefined;
    let disabled = false;
    let buttonText = "Scan Image"

    let url = ""
    let previewFile: HTMLImageElement
    let fileName: string
    let fileInput: HTMLInputElement | null
    let file: File | undefined;
    function previewFileFromLocal() {
        fileInput = document.querySelector("input[type=file]");
        if (!fileInput) return;

        if (fileInput.files) {
            file = fileInput.files[0];
        }

        let reader = new FileReader();
        reader.onload = function () {
            previewFile.src = reader.result as string;
        }

        if (file) {
            reader.readAsDataURL(file);
        } else {
            previewFile.src = "";
        }
    }
    async function predictFromUpload(){
        content = undefined;
        disabled = true;
        buttonText = "Please wait..."
        url = "";

        let formData = new FormData();
        if (file) {
            formData.append("file", file);
        }

        const response = await fetch("/predict-from-upload", {
            method: "POST",
            body: formData,
        });

        content = await response.text();
        disabled = false;
        buttonText = "Scan Image"
    }
    async function predictFromURL(){
        content = undefined;
        disabled = true;
        buttonText = "Please wait..."
        fileInput = null;

        let formData = new FormData();
        if (file) {
            formData.append("file", file);
        }

        const response = await fetch("/predict-from-url", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                url,
            }),
        });

        content = await response.text();
        disabled = false;
        buttonText = "Scan Image"
    }
    function example1(){
        url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnPz9iNt6sUJyLJ0zn9b50tGKlqxV2WJEkLA&s"
    }
    function example2(){
        url = "https://www.structuremag.org/app/uploads/2024/05/0615-ps-1.jpg"
    }
</script>

<svelte:head>
    <title>
        Concrete Crack Prediction Powered by AI
    </title>
</svelte:head>

<div class="mx-auto grid w-full max-w-2xl gap-2">
    <h1 class="text-2xl font-semibold">Concrete Crack Predictor</h1>
</div>

<div
  class="mx-auto grid w-full max-w-2xl items-start gap-6 md:grid-cols-1 lg:grid-cols-1"
>
    <div class="grid gap-6">
        <Card.Root>
            <Card.Header>
                <Card.Title>AI-Powered Detection for Safer Structures</Card.Title>
                <Card.Description>
                    Detect cracks in concrete instantly using AI-powered image analysis. Fast, accurate, and reliable detection to help you maintain safer structures.
                    Upload your concrete surface picture to predict if it has cracks.
                </Card.Description>
            </Card.Header>
            <Card.Content>
                <form class="flex flex-col gap-4">
                    <Tabs.Root value="url" class="w-full">
                        <Tabs.List class="grid w-full grid-cols-3">
                            <Tabs.Trigger value="url">URL</Tabs.Trigger>
                            <Tabs.Trigger value="upload">Upload</Tabs.Trigger>
                            <Tabs.Trigger value="about">About</Tabs.Trigger>
                        </Tabs.List>
                        <Tabs.Content value="url">
                            <Card.Root>
                                <Card.Header>
                                <Card.Title>From URL</Card.Title>
                                <Card.Description>
                                    Detect from an image URL.
                                </Card.Description>
                                </Card.Header>
                                <Card.Content class="space-y-2">
                                    <div class="space-y-1">
                                        <Label for="name">Link</Label>
                                        <Input id="name" bind:value={url} placeholder="https://www.structuremag.org/app/uploads/2024/05/0615-ps-1.jpg" />
                                    </div>
                                    {#if url}
                                        <img src={url} height="200" width="200" alt="">
                                    {/if}
                                    <div>
                                        <small class="text-sm font-medium leading-none">
                                            Try:
                                        </small>
                                        <small class="text-sm font-medium leading-none">
                                            <a href="" on:click={example1}>Example 1</a>
                                        </small>
                                        <small class="text-sm font-medium leading-none">
                                            <a href="" on:click={example2}>Example 2</a>
                                        </small>
                                    </div>
                                </Card.Content>
                                <Card.Footer>
                                    <Button on:click={predictFromURL} {disabled}>
                                        {#if disabled}
                                            <Reload class="mr-2 h-4 w-4 animate-spin" />
                                        {/if}
                                        {buttonText}
                                    </Button>
                                </Card.Footer>
                            </Card.Root>
                        </Tabs.Content>
                        <Tabs.Content value="upload">
                            <Card.Root>
                                <Card.Header>
                                <Card.Title>Upload</Card.Title>
                                <Card.Description>
                                    Upload from your local device.
                                </Card.Description>
                                </Card.Header>
                                <Card.Content class="space-y-2">
                                    <div class="space-y-1">
                                        <Label for="picture">File</Label>
                                        <Input id="picture" type="file" on:change={previewFileFromLocal} bind:value={fileName} />
                                    </div>
                                    {#if fileName}
                                        <img src="" height="200" width="200" alt="" bind:this={previewFile}>
                                    {/if}
                                </Card.Content>
                                <Card.Footer>
                                    <Button on:click={predictFromUpload} {disabled}>
                                        {#if disabled}
                                            <Reload class="mr-2 h-4 w-4 animate-spin" />
                                        {/if}
                                        {buttonText}
                                    </Button>
                                </Card.Footer>
                            </Card.Root>
                        </Tabs.Content>
                        <Tabs.Content value="about">
                            <Card.Root>
                                <Card.Header>
                                    <Card.Title>Concrete Crack Predictor</Card.Title>
                                </Card.Header>
                                <Card.Content class="space-y-2">
                                    <Label for="name">Author</Label><br>
                                    <a href="https://dukenmarga.id">Duken Marga</a>
                                    <Separator class="my-4" />

                                    <Label for="name">Training Dataset</Label><br>
                                    <a href="https://data.mendeley.com/datasets/z93rb2m4fk/1">
                                        Nyathi, Mthabisi Adriano; Bai, Jiping; Wilson, Ian David (2024), “NYA-Crack-Data: A High Variability Concrete Crack Dataset for Enhanced Model Generalisation”, Mendeley Data, V1, doi: 10.17632/z93rb2m4fk.1
                                    </a>
                                    <Separator class="my-4" />

                                    <Label for="name">Pretrained Models</Label><br>
                                    <a href="https://pytorch.org/vision/main/models/generated/torchvision.models.resnet18.html">
                                        Resnet18
                                    </a>
                                    <Separator class="my-4" />

                                    <Label for="name">Limitation</Label><br>
                                        Thin/small cracks may not be detected.
                                </Card.Content>
                            </Card.Root>
                        </Tabs.Content>
                    </Tabs.Root>
                </form>
            </Card.Content>
            <!-- <Card.Footer class="border-t px-6 py-4">
            </Card.Footer> -->
        </Card.Root>
        {#if content}
        <Card.Root>
            <Card.Header>
                <Card.Title>Analysis Results</Card.Title>
            </Card.Header>
            <Card.Content>
                {@html content}
            </Card.Content>
        </Card.Root>
        {/if}
    </div>
</div>