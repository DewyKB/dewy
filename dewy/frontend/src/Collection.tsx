import {
    List,
    Datagrid,
    TextField,
    TopToolbar,
    FilterButton,
    SearchInput,
    EditButton,
    CreateButton,
    Create,
    Edit,
    SimpleForm,
    CheckboxGroupInput,
    TextInput,
    SelectInput,
    required
} from 'react-admin';

const ListActions = () => (
    <TopToolbar>
        <CreateButton/>
    </TopToolbar>
);
export const CollectionList = () => (
    <List actions={<ListActions/>} >
        <Datagrid>
            <TextField source="name" />
            <TextField source="text_embedding_model" />
            <TextField source="text_distance_metric" />
            <TextField source="llm_model" />
        </Datagrid>
    </List>
);

export const ChunkingConfig = () => (
    <>
        <CheckboxGroupInput label="Chunks to Extract" source="extract" defaultValue={["snippets"]} choices={[
            {id: "snippets", name: "Snippets"},
            {id: "summaries", name: "Summaries"},
            {id: "images", name: "Images"}
        ]}/>
        <CheckboxGroupInput label="Retrieve Using" source="index"  defaultValue={["text"]} choices={[
            {id: "text", name: "Text"},
            {id: "questions_answered", name: "Questions Answered"},
            {id: "statements", name: "Statements"},
        ]}/>
    </>
)

const Form = () => (
    <SimpleForm>
        <TextInput source="name" validate={[required()]} fullWidth />
        <SelectInput source="text_embedding_model" defaultValue="hf:BAAI/bge-small-en" choices={[
            {id: 'hf:BAAI/bge-small-en', name: 'BAAI/bge-small-en'},
            {id: 'openai:text-embedding-ada-002', name: 'OpenAI/text_embedding_ada_002'},
        ]}/>
        <SelectInput source="text_distance_metric" defaultValue="cosine" choices={[
            {id: 'cosine', name: 'Cosine'},
            {id: 'ip', name: 'Inner Product'},
            {id: 'l2', name: 'L2-Norm'},
        ]}/>
        <SelectInput source="llm_model" defaultValue="huggingface:StabilityAI/stablelm-tuned-alpha-3b" choices={[
            {id: 'huggingface:StabilityAI/stablelm-tuned-alpha-3b', name: 'stablelm-tuned-alpha-3b'},
            {id: 'openai:gpt-3.5-turbo', name: 'gpt-3.5-turbo'},
        ]}/>
        <ChunkingConfig />
    </SimpleForm>
)

export const CollectionCreate = () => (
    <Create redirect="list">
        <Form/>
    </Create>
);

export const CollectionEdit = () => (
    <Edit redirect="list">
        <Form/>
    </Edit>
);
