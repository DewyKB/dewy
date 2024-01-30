import { Menu } from 'react-admin';
import SearchIcon from '@mui/icons-material/Search';

export const MyMenu = () => (
    <Menu>
        <Menu.ResourceItems />
        <Menu.Item to="/search" primaryText="Search" leftIcon={<SearchIcon />}/>
    </Menu>
);