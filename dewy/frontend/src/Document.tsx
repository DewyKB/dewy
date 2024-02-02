import { 
    List,
    Datagrid,
    ChipField,
    TextField,
    ReferenceManyField,
    Show,
    SimpleShowLayout,
    ReferenceField,
    BooleanField,
    FileField,
    TopToolbar,
    EditButton,
    ShowButton,
    FilterButton,
    CreateButton,
    SearchInput,
    Create,
    Edit,
    SimpleForm,
    SelectInput,
    ReferenceInput,
    RichTextField,
    FileInput,
    required,
    TextInput
} from 'react-admin';

import { ChunkingConfig } from "./Collection";

const ListActions = () => (
    <TopToolbar>
        <FilterButton/>
        <CreateButton/>
    </TopToolbar>
);

const listFilters = [
    <ReferenceInput source="collection_id" reference="collections"/>,
];

export const DocumentList = () => (
    <List actions={<ListActions/>} filters={listFilters} >
        <Datagrid>
            <TextField source="url" />
            <>
            <ShowButton />
            <EditButton />
            </>
        </Datagrid>
    </List>
);


export const DocumentCreate = () => (
    <Create redirect="list">
        <SimpleForm>
            <ReferenceInput source="collection_id" reference="collections" />
            <TextInput source="url"/>
        </SimpleForm>
    </Create>
);

export const DocumentEdit = () => (
    <Edit redirect="list">
    <SimpleForm>
        <TextInput source="url"/>
    </SimpleForm>
    </Edit>
);

export const DocumentShow = () => (
    <Show>
        <SimpleShowLayout>
            <TextField source="url" />
            <RichTextField source="text" />
            <ReferenceManyField label="Chunk" reference="chunks" target="document_id">
              <Datagrid>
                <ChipField source="kind"/>
                <TextField source="text" sx={{overflow: "hidden", textOverflow: "ellipsis", display: "-webkit-box", WebkitLineClamp: "3", WebkitBoxOrient: "vertical"}}/>
                <ShowButton/>
              </Datagrid>
            </ReferenceManyField>
        </SimpleShowLayout>
    </Show>
);