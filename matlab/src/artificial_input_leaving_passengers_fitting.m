%% leaving passengers
% 
% %% Transforming the leaving passengers dataset into percentages
% sum1=0;
% j=1;
% global_validation_leaving_percen=[];
% while j<=length(global_validation_dataset)
%     
%         for i=j: j+8
%             % Column 4 depicts the number of leaving passengers in this station
%             sum=sum+global_validation_dataset(i,4);
%             % Coloumn 5 is the number of leaving passengers
%             if (sum1~=0)
%                 global_validation_leaving_percen(i)= global_validation_dataset(i,5)/sum;
%                 
%             else
%                 global_validation_leaving_percen(i)=0;
%             end
%             sum1=sum1-global_validation_dataset(i,5);
%         end
%         j=i+1;
%   
%     sum1=0;
% end
%  
% global_validation_leaving_percen=global_validation_leaving_percen';
% % zeros where the percentage is more than 1 due to incosistent dataset
% global_validation_leaving_percen(global_validation_leaving_percen(:)>1)=1;

%% Fitting process
% for every station all the days for each direction
X=[];
exit_percentage_artificial_data=zeros(9,2);
for i=1: 9
    
        %After 9 steps appears the same station
        for j=i:9 :length(global_validation_leaving_percen)
            %checking for the direction
            if (global_validation_dataset(j,1)==1)
                X=[X;global_validation_leaving_percen(j)];
            end
        end
        if sum(X)~=0
            [PHAT, PCI] = betafit(X, 0.05);
            exit_percentage_artificial_data(i,:) = [PHAT(1), PHAT(2)];
        else
            exit_percentage_artificial_data(i,:)=0;
        end
end