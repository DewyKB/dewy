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
    TextInput,
    TabbedForm,
    TabbedShowLayout
} from 'react-admin';

import { ChunkingConfig } from "./Collection";

const ListActions = () => (
    <TopToolbar>
        <FilterButton/>
        <CreateButton/>
    </TopToolbar>
);

const listFilters = [
    <ReferenceInput source="collection" reference="collections"/>,
];

export const DocumentList = () => (
    <List actions={<ListActions/>} filters={listFilters} >
        <Datagrid>
            <TextField source="url" />
            <TextField source="ingest_state" />
            <TextField source="ingest_error" />
            <>
            <ShowButton />
            <EditButton />
            </>
        </Datagrid>
    </List>
);


export const DocumentCreate = () => (
    <Create redirect="list">
        <TabbedForm>
            <TabbedForm.Tab label="File">
                <ReferenceInput source="collection" reference="collections" />
                <FileInput source="file">
                    <FileField source="src" title="title" />
                </FileInput>
            </TabbedForm.Tab>
            <TabbedForm.Tab label="URL">
                <ReferenceInput source="collection" reference="collections" />
                <TextInput source="url"/>
            </TabbedForm.Tab>
        </TabbedForm>
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
