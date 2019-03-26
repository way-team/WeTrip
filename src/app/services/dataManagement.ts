import { test, User, City } from './../app.data.model';
import { Injectable } from "@angular/core";
import { RestWS } from "./restService";

@Injectable()
export class DataManagement {
	constructor(private restService: RestWS) { }

	public login(credentials): Promise<any> {
		return this.restService
			.login(credentials)
			.then(data => {
				return Promise.resolve(data);
			})
			.catch(error => {
				return Promise.reject('error');
			});
	}

	public getUserLogged(token): Promise<any> {
		return this.restService
			.getUserLogged(token)
			.then(data => {
				return Promise.resolve(data);
			})
			.catch(error => {
				return Promise.reject(error);
			});
	}

	public hasConnection(): boolean {
		return true;
	}

	public test(): Promise<test> {
		return new Promise((resolve, reject) => {
			if (this.hasConnection()) {
				return this.restService
					.test()
					.then((data: test) => {
						resolve(data);
					})
					.catch(error => {
						reject('error');
					});
			} else {
				reject('error');
			}
		});
	}

	public listFriends(): Promise<any> {
		return new Promise((resolve, reject) => {
			if (this.hasConnection()) {
				return this.restService
					.listFriends()
					.then((data: any) => {
						resolve(data);
					})
					.catch(error => {
						reject('error');
					});
			} else {
				reject('error');
			}
		});
	}

	public listYourTrips(): Promise<any> {
		return new Promise((resolve, reject) => {
			if (this.hasConnection()) {
				return this.restService.listYourTrips().then((data: any) => {
					resolve(data);
				}).catch((error) => {
					reject('error');
				})
			} else {
				reject('error');
			}
		});
	}


	public listMeetYou(): Promise<any> {
		return new Promise((resolve, reject) => {
			if (this.hasConnection()) {
				return this.restService
					.listMeetYou()
					.then((data: any) => {
						resolve(data);
					})
					.catch(error => {
						reject('error');
					});
			} else {
				reject('error');
			}
		});
	}

	public createTrip(title: string, description: string, start_date: Date, end_date: Date, trip_type: string, image: string, city: City): Promise<any> {
		return this.restService.createTrip(title, description, start_date, end_date, trip_type, image, city).then((data) => {
			return Promise.resolve(data);
		}).catch((error) => {
			return Promise.reject('error');
		})
	}


}
