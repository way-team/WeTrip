import { HttpClient } from '@angular/common/http';
import { ConfigService } from './../../config/configService';
import { AbstractWS } from './abstractService';
import { Injectable } from '@angular/core';
import { User, Trip, UserProfile } from '../app.data.model';

@Injectable()
export class RestWS extends AbstractWS {
  path: string = '';

  constructor(private config: ConfigService, http: HttpClient) {
    super(http);
    // this.path = this.config.config().restUrlPrefix;
    this.path = this.config.config().restUrlPrefixLocalhost;
  }
  //Methods
  public login(credentials) {
    const fd = new FormData();
    fd.append('username', credentials.username);
    fd.append('password', credentials.password);
    return this.makePostRequest(this.path + 'login/', fd)
      .then(res => {
        console.log('Logged successfully');
        return Promise.resolve(res);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public test(): Promise<any> {
    let requestParams = {
      text: 'texto'
    };

    return this.makeGetRequest(this.path + 'users/', requestParams)
      .then((res: any) => {
        return Promise.resolve(res);
      })
      .catch(error => {
        return Promise.reject(error);
      });
  }
  public getUserLogged(token) {
    const fd = new FormData();
    fd.append('token', token);
    return this.makePostRequest(this.path + 'getUserByToken/', fd)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(err => {
        console.log('Error: ' + err);
        return Promise.reject(err);
      });
  }

  public listFriends(): Promise<any> {
    return null;
  }

  public listMeetYou(): Promise<any> {
    let meetYou: User[] = [];
    let user1: User = {
      name: 'User 4',
      photo: '../../../assets/img/avatar5.jpeg',
      description: 'nature is waiting for me!',
      username: null,
      email: null,
      password: null,
      lastName: null,
      birthdate: null,
      gender: null,
      nationality: null,
      city: null,
      status: null,
      mediumRate: null,
      numRate: null,
      isPremium: null,
      isSuperUser: null
    };
    let user2: User = {
      name: 'User 5',
      photo: '../../../assets/img/avatar6.jpeg',
      description: 'only english language',
      username: null,
      email: null,
      password: null,
      lastName: null,
      birthdate: null,
      gender: null,
      nationality: null,
      city: null,
      status: null,
      mediumRate: null,
      numRate: null,
      isPremium: null,
      isSuperUser: null
    };
    let user3: User = {
      name: 'User 6',
      photo: '../../../assets/img/avatar7.jpeg',
      description: 'I want to go to Australia',
      username: null,
      email: null,
      password: null,
      lastName: null,
      birthdate: null,
      gender: null,
      nationality: null,
      city: null,
      status: null,
      mediumRate: null,
      numRate: null,
      isPremium: null,
      isSuperUser: null
    };

    meetYou.push(user1, user2, user3);
    // return this.makeGetRequest(this.path + "users/", null).then((friends: any) => {
    //     return Promise.resolve(friends);
    // }).catch((error) => {
    //     return Promise.reject(error);
    // });
    return Promise.resolve(meetYou);
  }

  public listYourTrips(): Promise<any> {
    let trips: Trip[] = [];
    let trip1: Trip = {
      title: 'Trip to Canada',
      description: 'Only adults',
      startDate: null,
      endDate: null,
      type: null,
      image: '../../../assets/img/trip_1.jpeg',
      status: null,
      country: 'Canada',
      city: 'Montreal'
    };

    let trip2: Trip = {
      title: 'Trip to NY',
      description: 'To families',
      startDate: null,
      endDate: null,
      type: null,
      image: '../../../assets/img/trip_2.jpeg',
      status: null,
      country: 'USA',
      city: 'New York'
    };
    trips.push(trip1, trip2);
    // return this.makeGetRequest(this.path + "trips/", null).then((trips: any) => {
    //     return Promise.resolve(trips);
    // }).catch((error) => {
    //     return Promise.reject(error);
    // });
    return Promise.resolve(trips);
  }
}
