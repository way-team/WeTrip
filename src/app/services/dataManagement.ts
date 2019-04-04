import { test, User, City, Trip } from './../app.data.model';
import { Injectable } from '@angular/core';
import { RestWS } from './restService';

@Injectable()
export class DataManagement {
  constructor(private restService: RestWS) {}

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

  public getUserBy(username, token): Promise<any> {
    return this.restService
      .getUserBy(username, token)
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
        return this.restService
          .listYourTrips()
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

  public listSearchTrips(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listSearchTrips()
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

  public listDiscover(): Promise<any> {
    return new Promise((resolve, reject) => {
      if (this.hasConnection()) {
        return this.restService
          .listDiscover()
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

  public createTrip(
    title: string,
    description: string,
    start_date: String,
    end_date: String,
    trip_type: string,
    city: Number,
    userImage
  ): Promise<any> {
    return this.restService
      .createTrip(
        title,
        description,
        start_date,
        end_date,
        trip_type,
        city,
        userImage
      )
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
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
    return this.restService
      .editTrip(
        id,
        title,
        description,
        start_date,
        end_date,
        trip_type,
        city,
        userImage
      )
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }


  public listCities(): Promise<any> {
    return this.restService
      .listCities()
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public getTripById(id: string): Promise<Trip> {
    return this.restService.getTripById(id).then(response => {
      return Promise.resolve(response);
    }).catch(error => {
      return Promise.reject(error);
    });
  }

  public sendMessage(sender: string,receiver: string,message: string): Promise<any> {
    return this.restService
      .sendMessage(sender, receiver, message)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }

  public getMessages(senderId: Number, receiverId: Number): Promise<any> {
    return this.restService
      .getMessages(senderId, receiverId)
      .then(data => {
        return Promise.resolve(data);
      })
      .catch(error => {
        return Promise.reject('error');
      });
  }
}
