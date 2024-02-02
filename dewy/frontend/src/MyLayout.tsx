import { Layout } from 'react-admin';
import { MyMenu } from './MyMenu';

export const MyLayout = (props) => <Layout {...props} menu={MyMenu} />;