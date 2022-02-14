import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import { throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import {API_URL} from '../env';
import {Exam} from './exam.model';

@Injectable()
export class ExamsApiService {

  constructor(private http: HttpClient) {
  }

  getExams(): Observable<Exam[]> {
    return this.http.get<Exam[]>(`${API_URL}/exams`).pipe(catchError(this.errorHandler));
  }

  errorHandler(error: HttpErrorResponse) {
    return throwError(error.message || 'server Error');
  }

}