%% variables modification
%normal direction cs->azu
%flip from right to left so that stations from both directions match:
AZU_CS_entering_flipped=fliplr(AZU_CS_entering);

%% entering passengers
timing_entering_global=[];
entering_global=[];

entering_global=[AZU_CS_entering_flipped ; CS_AZU_entering];
timing_entering_global=[timing_AZU_CS ; timing_CS_AZU];
[timing_entering_global,indices]=sort(timing_entering_global);
entering_global=entering_global(indices,:);



%% leaving passengers
%normal direction cs->azu
%flip from right to left the stations:
AZU_CS_leaving_flipped=fliplr(AZU_CS_leaving);

leaving_global=[AZU_CS_leaving_flipped;CS_AZU_leaving];
timing_leaving_global=[timing_AZU_CS;timing_CS_AZU];
[timing_leaving_global,indices2]=sort(timing_leaving_global);
leaving_global=leaving_global(indices2,:);

%% leaving passengers transformation into percentages

AZU_CS_leaving_percen=[];
sum=0;
for i=1:length(AZU_CS_leaving)
    for j=1:9
        sum=sum+AZU_CS_entering(i,j);
        AZU_CS_leaving_percen(i,j)=(AZU_CS_leaving(i,j)/sum )* 100;
        if (sum==0)
            AZU_CS_leaving_percen(i,j)=0;
        else
            sum=sum-AZU_CS_leaving(i,j);
        end
    end
    sum=0;

end


CS_AZU_leaving_percen=[];
sum=0;
for i=1:length(CS_AZU_leaving)
    for j=1:9
        sum=sum+CS_AZU_entering(i,j);
        CS_AZU_leaving_percen(i,j)=(CS_AZU_leaving(i,j)/sum )* 100;
        if (sum==0)
            CS_AZU_leaving_percen(i,j)=0;
        else
            sum=sum-CS_AZU_leaving(i,j);
        end
    end
    sum=0;

end
%% sorting
leaving_global_percen=[AZU_CS_leaving_percen;CS_AZU_leaving_percen];
leaving_global_percen=leaving_global_percen(indices2,:);

clear sum i j;





