import { test } from './../app.data.model';
import { Injectable } from "@angular/core";
import { RestWS } from "./restService";

@Injectable()
export class DataManagement {

	constructor(private restService: RestWS,
	) {

	}

	public hasConnection(): boolean {
		return true;
	}

	public test(): Promise<test> {
		return new Promise((resolve, reject) => {
			if (this.hasConnection()) {
				return this.restService.test().then((data: test) => {
					resolve(data);
				}).catch((error) => {
					reject('error');
				})
			} else {
				reject('error');
			}
		});
	}

}
