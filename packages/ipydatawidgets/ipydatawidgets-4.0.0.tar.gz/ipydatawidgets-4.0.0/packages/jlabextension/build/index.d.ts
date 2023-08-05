import { Application, IPlugin } from '@phosphor/application';
import { Widget } from '@phosphor/widgets';
import { Token } from '@phosphor/coreutils';
/**
 * The token identifying the JupyterLab plugin.
 */
export declare const IDataWidgetsExtension: Token<IDataWidgetsExtension>;
/**
 * The type of the provided value of the plugin in JupyterLab.
 */
export interface IDataWidgetsExtension {
}
/**
 * The notebook diff provider.
 */
declare const dataWidgetsProvider: IPlugin<Application<Widget>, IDataWidgetsExtension>;
export default dataWidgetsProvider;
//# sourceMappingURL=index.d.ts.map