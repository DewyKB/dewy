import { 
    List,
    Datagrid,
    TextField,
    ReferenceField,
    BooleanField,
    FileField,
    TopToolbar,
    EditButton,
    FilterButton,
    CreateButton,
    SearchInput,
    Create,
    Edit,
    SimpleForm,
    SelectInput,
    ReferenceInput,
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