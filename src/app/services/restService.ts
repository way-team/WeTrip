import { HttpClient } from '@angular/common/http';
import { ConfigService } from './../../config/configService';
import { AbstractWS } from './abstractService';
import { Injectable } from '@angular/core';
import { User, Trip, UserProfile, City } from '../app.data.model';
import { CookieService } from 'ngx-cookie-service';

@Injectable()
export class RestWS extends AbstractWS {
  path = '';

  constructor(
    private config: ConfigService,
    http: HttpClient,
    private cookieService: CookieService
  ) {
    super(http);
    // this.path = this.config.config().restUrlPrefix;
    this.path = this.config.config().restUrlPrefixLocalhost;
  }
  // Methods
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
    const requestParams = {
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

  public getUserBy(username, token) {
    return this.makeGetRequest(
      this.path + 'users/' + username + '/',
      null,
      token
    )
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(err => {
        console.log('Error: ' + err);
        return Promise.reject(err);
      });
  }

  public listFriends(): Promise<any> {
    let token = this.cookieService.get('token');
    const fd = new FormData();
    fd.append('token', token);
    return this.makePostRequest(this.path + 'getFriends/', fd)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public listDiscover(): Promise<any> {
    let token = this.cookieService.get('token');
    const fd = new FormData();
    fd.append('token', token);
    return this.makePostRequest(this.path + 'getDiscoverPeople/', fd)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public listMeetYou(): Promise<any> {
    let token = this.cookieService.get('token');
    const fd = new FormData();
    fd.append('token', token);
    return this.makePostRequest(this.path + 'getPending/', fd)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public listYourTrips(): Promise<any> {
    const Authorization = this.cookieService.get('token');

    return this.makeGetRequest(
      this.path + 'trips/myTrips/',
      null,
      Authorization
    )
      .then(res => {
        return Promise.resolve(res.results);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public listSearchTrips(): Promise<any> {
    const Authorization = this.cookieService.get('token');

    return this.makeGetRequest(
      this.path + 'trips/',
      null,
      Authorization
    )
      .then(res => {
        return Promise.resolve(res.results);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }


  public createTrip(
    title: string,
    description: string,
    start_date: String,
    end_date: String,
    trip_type: string,
    city: Number,
    userImage
  ): Promise<any> {
    const fd = new FormData();
    let user: User;
    let token: string;
    token = this.cookieService.get('token');
    return this.getUserLogged(token)
      .then(res => {
        fd.append('title', title);
        fd.append('description', description);
        fd.append('start_date', String(start_date));
        fd.append('end_date', String(end_date));
        fd.append('trip_type', trip_type);
        fd.append('city', String(city));
        if (userImage !== null) {
          fd.append('file', userImage, userImage.name);
        }

        user = res;
        fd.append('user_id', String(user.id));

        return this.makePostRequest(this.path + 'createTrip/', fd, token)
          .then(res2 => {
            console.log('Se ha creado exitosamente');
            return Promise.resolve(res2);
          })
          .catch(error => {
            console.log('Error: ' + error);
            return Promise.reject(error);
          });
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public editTrip(
    id: String,
    title: string,
    description: string,
    start_date: String,
    end_date: String,
    trip_type: string,
    city: Number,
    userImage
  ): Promise<any> {
    const fd = new FormData();
    let user: User;
    let token: string;
    token = this.cookieService.get('token');
    return this.getUserLogged(token)
      .then(res => {
        fd.append('trip_id', String(id));
        fd.append('title', title);
        fd.append('description', description);
        fd.append('start_date', String(start_date));
        fd.append('end_date', String(end_date));
        fd.append('trip_type', trip_type);
        fd.append('city', String(city));
        if (userImage !== null) {
          fd.append('file', userImage, userImage.name);
        }

        user = res;
        fd.append('user_id', String(user.id));

        return this.makePostRequest(this.path + 'editTrip/', fd, token)
          .then(res2 => {
            console.log('Se ha creado exitosamente');
            return Promise.resolve(res2);
          })
          .catch(error => {
            console.log('Error: ' + error);
            return Promise.reject(error);
          });
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }

  public listCities(): Promise<any> {
    const token = this.cookieService.get('token');
    return this.makeGetRequest(this.path + 'list-cities/', false, token)
      .then(res => {
        return Promise.resolve(res);
      })
      .catch(error => {
        console.log('Error: ' + error);
        return Promise.reject(error);
      });
  }
}
