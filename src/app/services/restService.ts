import { HttpClient } from '@angular/common/http';
import { ConfigService } from './../../config/configService';
import { AbstractWS } from './abstractService';
import { Injectable } from '@angular/core';



@Injectable()
export class RestWS extends AbstractWS {
    path:string = "";

    constructor(
        private config: ConfigService,
        http: HttpClient
    ) {
        super(http);
        this.path = this.config.config().restUrlPrefix;
    }

    public test(): Promise<any> {
        let requestParams = {
            "text": "texto"
        };

        return this.makeGetRequest(this.path + "users/", requestParams).then((res: any) => {
            return Promise.resolve(res);
        }).catch((error) => {
            return Promise.reject(error);
        });
    }
}
