import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';


@Injectable()
export class ConfigService {
	constructor() { }

	public config() {
		let urlPrefix = 'http://192.168.1.135:8000/';
		let urlAPI = '';
		if (environment.production) {
			urlPrefix = 'https://herokuapp.com/nuestraAppEsLaCanya/'
			urlAPI = 'api/v1/'
		}
		// pathFiles for Storage provider
		let pathFiles = '/assets/storageFiles';
		// myCustomVars
		let myCustomVars1 = 123;
		let myCustomVars2 = 456;
		return {
			restUrlPrefix: urlPrefix + urlAPI,
			destPathFiles: pathFiles,
			myCustomVars1: myCustomVars1,
			myCustomVars2: myCustomVars2
		};
	}

}
