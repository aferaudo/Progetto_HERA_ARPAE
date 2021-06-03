USE [Hera]
GO

/****** Object:  Table [dbo].[coord_pluv]    Script Date: 4/20/2021 8:28:26 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[coord_pluv_ex](
	[cod_pluv] [nvarchar](50) NOT NULL,
	[lat] [float] NOT NULL,
	[long] [float] NOT NULL,
	[territorio] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_coord_pluv_ex] PRIMARY KEY CLUSTERED 
(
	[cod_pluv] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


