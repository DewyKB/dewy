---
title: Using the API
sidebar_position: 4
--- 

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Using the API


## Install the API client library

<Tabs groupId="language">
    <TabItem value="typescript" label="typescript" default>
    ```sh
    npm install dewy-ts
    ```
    </TabItem>
    <TabItem value="python" label="python">
    ```sh
    pip install dewy-py
    ```
    </TabItem>
</Tabs>

## Connect to an instance of Dewy

<Tabs groupId="language">
    <TabItem value="typescript">
    ```typescript
    import { Dewy } from 'dewy_ts';
    const dewy = new Dewy()
    ```
    </TabItem>
</Tabs>

## Add documents
    ```typescript
    await dewy.default.addDocument({
      collection_id: 1,
      url: 'https://arxiv.org/abs/2005.11401',
    })
    ```

## Retrieve document chunks for LLM prompting

<Tabs groupId="language">
    <TabItem value="typescript">
    ```typescript
    const context = await dewy.default.retrieveChunks({
      collection_id: 1,
      query: "tell me about RAG", 
      n: 10,
    });

    // Minimal prompt example
    const prompt = [
      {
        role: 'system',
        content: `You are a helpful assistant.
        You will take into account any CONTEXT BLOCK that is provided in a conversation.
        START CONTEXT BLOCK
        ${context.results.map((c: any) => c.chunk.text).join("\n")}
        END OF CONTEXT BLOCK
        `,
      },
    ]

    // Using OpenAI to generate responses
    const response = await openai.chat.completions.create({
      model: 'gpt-3.5-turbo',
      stream: true,
      messages: [...prompt, [{role: 'user': content: 'Tell me about RAG'}]]
    })
    ```
    </TabItem>
</Tabs>